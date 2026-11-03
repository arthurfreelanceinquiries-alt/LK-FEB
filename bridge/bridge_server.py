#!/usr/bin/env python3
"""
LK-FEB BRIDGE SERVER
====================
Jembatan lokal antara Telegram Executive Remote, mesin multi-akun Antigravity,
dan Portal LK-FEB BEM FEB UKRIDA.

Fitur utama:
  * GET  /api/status                  -> status akun, bot, rapat, notulensi
  * POST /api/antigravity/switch      -> pindah profil akun Antigravity
  * POST /api/antigravity/run         -> jalankan instruksi via Antigravity
  * GET  /api/meetings                -> daftar rapat + reminder
  * POST /api/meetings                -> tambah rapat / reminder
  * GET  /api/notulensi               -> daftar notulensi Second Brain
  * OPTIONS *                         -> CORS preflight untuk Portal LK-FEB

Hanya memakai Python standard library. Dijalankan pada port 9440.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import traceback
from datetime import date, datetime, time as dt_time, timedelta, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from urllib.parse import parse_qs, urlparse

# ---------------------------------------------------------------------------
# Identitas & lokasi
# ---------------------------------------------------------------------------

BRIDGE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BRIDGE_DIR.parent
CONFIG_DIR = BRIDGE_DIR / "config"
DATA_DIR = Path(os.environ.get("LK_FEB_BRIDGE_DATA_DIR", str(BRIDGE_DIR / "data")))
NOTULENSI_DIR = Path(
    os.environ.get(
        "LK_FEB_NOTULENSI_DIR", str(ROOT_DIR / "07_Second_Brain" / "notulensi")
    )
)

ACCOUNTS_PATH = CONFIG_DIR / "antigravity_accounts.json"
TELEGRAM_CONFIG_PATH = CONFIG_DIR / "telegram_config.json"
MEETINGS_PATH = DATA_DIR / "meetings.json"
TELEGRAM_STATUS_PATH = DATA_DIR / "telegram_status.json"
TELEGRAM_OFFSET_PATH = DATA_DIR / "telegram_offset.json"
CALENDAR_PATH = DATA_DIR / "bem_feb_calendar.ics"

HOST = os.environ.get("LK_FEB_BRIDGE_HOST", "127.0.0.1")
PORT = int(os.environ.get("LK_FEB_BRIDGE_PORT", "9440"))
DEFAULT_MODEL = os.environ.get(
    "LK_FEB_ANTIGRAVITY_MODEL", "antigravity/deepseek-v4.1-flash-free"
)

ORGANIZATION = "BEM FEB UKRIDA"
CAMPUS_ADDRESS = "Jl. Tanjung Duren Raya No. 4, Jakarta Barat"
SERVER_VERSION = "1.0.0"
STARTED_AT = time.time()

LOCK = threading.RLock()
SERVER_STATE: Dict[str, Any] = {}
SERVER_STATE_LOCK = threading.Lock()

MONTHS_ID = {
    "januari": 1,
    "jan": 1,
    "februari": 2,
    "feb": 2,
    "maret": 3,
    "mar": 3,
    "april": 4,
    "apr": 4,
    "mei": 5,
    "may": 5,
    "juni": 6,
    "jun": 6,
    "juli": 7,
    "jul": 7,
    "agustus": 8,
    "agu": 8,
    "agt": 8,
    "aug": 8,
    "september": 9,
    "sep": 9,
    "sept": 9,
    "oktober": 10,
    "okt": 10,
    "oct": 10,
    "november": 11,
    "nov": 11,
    "desember": 12,
    "des": 12,
    "dec": 12,
}

DAY_NAMES_ID = {
    "senin": 0,
    "selasa": 1,
    "rabu": 2,
    "kamis": 3,
    "jumat": 4,
    "jum'at": 4,
    "sabtu": 5,
    "minggu": 6,
    "ahad": 6,
}

DAY_NAMES_FULL = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
]

MONTHS_FULL = [
    "",
    "Januari",
    "Februari",
    "Maret",
    "April",
    "Mei",
    "Juni",
    "Juli",
    "Agustus",
    "September",
    "Oktober",
    "November",
    "Desember",
]


# ---------------------------------------------------------------------------
# Utilitas umum
# ---------------------------------------------------------------------------


def now_local() -> datetime:
    """Waktu lokal (Asia/Jakarta pada mesin BEM FEB)."""

    return datetime.now().astimezone()


def now_iso() -> str:
    return now_local().isoformat(timespec="seconds")


def clean_text(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if not isinstance(value, str):
        value = str(value)
    return value.strip()


def safe_int(value: Any, default: int) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def truncate(value: str, limit: int) -> str:
    value = clean_text(value)
    if len(value) <= limit:
        return value
    return value[: max(0, limit - 1)].rstrip() + "…"


def unique_id(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}-{os.urandom(2).hex()}"


def ensure_dirs() -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    NOTULENSI_DIR.mkdir(parents=True, exist_ok=True)


def read_json(path: Path, default: Any) -> Any:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except FileNotFoundError:
        return default
    except (json.JSONDecodeError, OSError) as exc:
        log(f"[WARN] Gagal membaca {path}: {exc}")
        return default


def atomic_write_text(path: Path, content: str, encoding: str = "utf-8") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(f".{path.name}.tmp.{os.getpid()}.{threading.get_ident()}")
    with temp.open("w", encoding=encoding, newline="\n") as handle:
        handle.write(content)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


def atomic_write_json(path: Path, payload: Any) -> None:
    text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
    atomic_write_text(path, text)


def log(message: str) -> None:
    timestamp = now_local().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)


def pid_is_alive(pid: Any) -> bool:
    try:
        pid_int = int(pid)
    except (TypeError, ValueError):
        return False
    if pid_int <= 0:
        return False
    try:
        os.kill(pid_int, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False


# ---------------------------------------------------------------------------
# Parser jadwal Bahasa Indonesia
# ---------------------------------------------------------------------------


def parse_schedule(raw: Any, default_date: Optional[date] = None) -> Dict[str, Any]:
    """
    Mengubah teks jadwal bebas (Indonesia) menjadi tanggal + waktu terstruktur.

    Contoh yang didukung:
      "Senin, 10 November 2026 16:00"
      "10 Nov 2026 16.00 - 18.00 WIB"
      "2026-11-10 16:00"
      "besok 09:00"
      "Kamis 15:30"
    """

    original = clean_text(raw)
    base = default_date or now_local().date()
    if isinstance(base, datetime):
        base = base.date()

    text = original.lower()
    parsed_date: Optional[date] = None
    date_spans: List[Tuple[int, int]] = []

    def set_date(year: int, month: int, day: int, span: Tuple[int, int]) -> None:
        nonlocal parsed_date, date_spans
        try:
            candidate = date(year, month, day)
        except ValueError:
            return
        parsed_date = candidate
        date_spans.append(span)

    # 1) ISO: YYYY-MM-DD / YYYY/MM/DD
    match = re.search(r"\b(\d{4})[-/](\d{1,2})[-/](\d{1,2})\b", text)
    if match:
        set_date(int(match.group(1)), int(match.group(2)), int(match.group(3)), match.span())

    # 2) DD NamaBulan YYYY
    if parsed_date is None:
        match = re.search(
            r"\b(\d{1,2})\s+([a-z]+)\.?\s+(\d{4})\b", text, flags=re.IGNORECASE
        )
        if match and match.group(2) in MONTHS_ID:
            set_date(
                int(match.group(3)),
                MONTHS_ID[match.group(2)],
                int(match.group(1)),
                match.span(),
            )

    # 3) NamaBulan DD, YYYY
    if parsed_date is None:
        match = re.search(
            r"\b([a-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})\b", text, flags=re.IGNORECASE
        )
        if match and match.group(1) in MONTHS_ID:
            set_date(
                int(match.group(3)),
                MONTHS_ID[match.group(1)],
                int(match.group(2)),
                match.span(),
            )

    # 4) DD/MM/YYYY atau DD-MM-YYYY
    if parsed_date is None:
        match = re.search(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b", text)
        if match:
            set_date(
                int(match.group(3)),
                int(match.group(2)),
                int(match.group(1)),
                match.span(),
            )

    # 5) Tanggal relatif / nama hari
    if parsed_date is None:
        if re.search(r"\blusa\b", text):
            parsed_date = base + timedelta(days=2)
        elif re.search(r"\b(besok|esok)\b", text):
            parsed_date = base + timedelta(days=1)
        elif re.search(r"\bhari\s+ini\b", text):
            parsed_date = base
        elif re.search(r"\bminggu\s+depan\b", text):
            parsed_date = base + timedelta(days=7)
        else:
            for day_name, weekday in DAY_NAMES_ID.items():
                if re.search(rf"\b{re.escape(day_name)}\b", text):
                    delta = (weekday - base.weekday()) % 7
                    parsed_date = base + timedelta(days=delta)
                    break

    # Siapkan sumber waktu tanpa memotong bagian tanggal yang mengandung titik.
    time_source = original
    for begin, end in sorted(date_spans, reverse=True):
        time_source = time_source[:begin] + " " + time_source[end:]
    time_source = re.sub(
        r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b", " ", time_source
    )
    time_source = re.sub(
        r"\b\d{1,2}[-/.]\d{1,2}[-/.]\d{4}\b", " ", time_source
    )

    time_matches = re.findall(
        r"(?<!\d)([01]?\d|2[0-3])[:.]([0-5]\d)(?!\d)", time_source
    )
    times = [f"{int(hour):02d}:{int(minute):02d}" for hour, minute in time_matches]

    start_time: Optional[str] = None
    end_time: Optional[str] = None
    if times:
        start_time = times[0]
        if len(times) >= 2:
            end_time = times[1]
        else:
            start_h, start_m = map(int, start_time.split(":"))
            end_dt = datetime.combine(date.today(), dt_time(start_h, start_m)) + timedelta(
                minutes=60
            )
            end_time = end_dt.strftime("%H:%M")

    final_date = parsed_date or base
    tzinfo = now_local().tzinfo

    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    if start_time:
        start_h, start_m = map(int, start_time.split(":"))
        start_at = datetime.combine(final_date, dt_time(start_h, start_m)).replace(
            tzinfo=tzinfo
        )
        end_h, end_m = map(int, end_time.split(":"))
        end_at = datetime.combine(final_date, dt_time(end_h, end_m)).replace(
            tzinfo=tzinfo
        )
        if end_at <= start_at:
            end_at = start_at + timedelta(hours=1)
            end_time = end_at.strftime("%H:%M")

    if start_time and end_time:
        canonical_time = f"{start_time} - {end_time} WIB"
    elif start_time:
        canonical_time = f"{start_time} WIB"
    elif parsed_date is None:
        canonical_time = original or "Waktu menyusul"
    else:
        leftover = re.sub(r"[\s,.\-|]+", " ", time_source).strip()
        if re.search(r"\b(pagi|siang|sore|malam|subuh)\b", leftover, re.IGNORECASE):
            canonical_time = leftover
        else:
            canonical_time = "Waktu menyusul"

    return {
        "tanggal": final_date.isoformat(),
        "waktu": canonical_time,
        "waktu_teks": original,
        "start_time": start_time,
        "end_time": end_time,
        "start_at": start_at.isoformat(timespec="seconds") if start_at else None,
        "end_at": end_at.isoformat(timespec="seconds") if end_at else None,
        "all_day": start_at is None,
        "date_explicit": parsed_date is not None,
    }


def format_tanggal_indonesia(value: Any) -> str:
    raw = clean_text(value)
    if not raw:
        return "—"
    try:
        parsed = date.fromisoformat(raw[:10])
    except ValueError:
        return raw
    return (
        f"{DAY_NAMES_FULL[parsed.weekday()]}, "
        f"{parsed.day} {MONTHS_FULL[parsed.month]} {parsed.year}"
    )


def derive_title(text: str, fallback: str = "Rapat BEM FEB UKRIDA") -> str:
    for line in clean_text(text).splitlines():
        candidate = re.sub(r"^[\s#>*\-\u2022\d.)]+", "", line).strip()
        if not candidate:
            continue
        candidate = re.sub(
            r"^(judul|agenda|topik|perihal)\s*[:\-]\s*",
            "",
            candidate,
            flags=re.IGNORECASE,
        ).strip()
        if candidate:
            return truncate(candidate, 110)
    return fallback


def extract_labeled_fields(text: str) -> Dict[str, str]:
    """Ambil metadata sederhana dari catatan bebas, mis. 'Tempat: Ruang Rapat'."""

    fields: Dict[str, str] = {}
    aliases = {
        "judul": "judul",
        "agenda": "agenda",
        "topik": "judul",
        "perihal": "judul",
        "tanggal": "tanggal",
        "hari": "tanggal",
        "waktu": "waktu",
        "tempat": "tempat",
        "lokasi": "tempat",
        "pimpinan": "pimpinan",
        "notulis": "notulis",
        "peserta": "peserta",
    }
    for line in clean_text(text).splitlines():
        match = re.match(r"^\s*([A-Za-z]+)\s*[:\-]\s*(.+?)\s*$", line)
        if not match:
            continue
        key = aliases.get(match.group(1).lower())
        if key and key not in fields:
            fields[key] = match.group(2).strip()
    return fields


# ---------------------------------------------------------------------------
# Registry akun Antigravity
# ---------------------------------------------------------------------------


def default_accounts_payload() -> Dict[str, Any]:
    stamp = now_iso()
    profiles = {
        "arthur_pro": {
            "id": "arthur_pro",
            "name": "Arthur Reezan (Google AI Pro)",
            "label": "Arthur Reezan (Google AI Pro)",
            "owner": "Arthur Reezan",
            "role": "Ketua BEM FEB UKRIDA (312023002)",
            "plan": "Google AI Pro",
            "provider": "google-antigravity",
            "config_path": "~/.config/Antigravity",
            "status": "active",
            "enabled": True,
            "hand_me_down": False,
            "notes": "Akun utama Ketua BEM FEB UKRIDA.",
            "created_at": stamp,
            "last_switched_at": stamp,
            "switch_count": 0,
        },
        "sekretariat": {
            "id": "sekretariat",
            "name": "Laptop Sekretariat BEM FEB",
            "label": "Laptop Sekretariat BEM FEB",
            "owner": "Sekretariat Jenderal BEM FEB",
            "role": "Sekretariat BEM FEB UKRIDA",
            "plan": "Google AI Pro",
            "provider": "google-antigravity",
            "config_path": "~/.config/antigravity-profiles/sekretariat",
            "status": "standby",
            "enabled": True,
            "hand_me_down": False,
            "notes": "Profil operasional laptop sekretariat.",
            "created_at": stamp,
            "last_switched_at": None,
            "switch_count": 0,
        },
        "bendahara": {
            "id": "bendahara",
            "name": "Laptop Bendahara BEM FEB",
            "label": "Laptop Bendahara BEM FEB",
            "owner": "Bendahara Umum BEM FEB",
            "role": "Bendahara BEM FEB UKRIDA",
            "plan": "Google AI Pro",
            "provider": "google-antigravity",
            "config_path": "~/.config/antigravity-profiles/bendahara",
            "status": "standby",
            "enabled": True,
            "hand_me_down": False,
            "notes": "Profil operasional laptop bendahara.",
            "created_at": stamp,
            "last_switched_at": None,
            "switch_count": 0,
        },
        "estafet_2027": {
            "id": "estafet_2027",
            "name": "Akun Pengurus Berikutnya (Hand-Me-Down)",
            "label": "Akun Pengurus Berikutnya (Hand-Me-Down)",
            "owner": "Pengurus BEM FEB 2027",
            "role": "Regenerasi Kepengurusan BEM FEB",
            "plan": "Google AI Pro",
            "provider": "google-antigravity",
            "config_path": "~/.config/antigravity-profiles/estafet_2027",
            "status": "standby",
            "enabled": True,
            "hand_me_down": True,
            "inherits_from": "arthur_pro",
            "successor_year": 2027,
            "notes": "Slot hand-me-down untuk pengurus berikutnya.",
            "created_at": stamp,
            "last_switched_at": None,
            "switch_count": 0,
        },
    }
    return {
        "schema_version": 1,
        "organization": ORGANIZATION,
        "description": "Registry akun Antigravity (BYOA / Hand-Me-Down) untuk Bridge LK-FEB.",
        "active_profile": "arthur_pro",
        "default_model": DEFAULT_MODEL,
        "updated_at": stamp,
        "profiles": profiles,
    }


def load_accounts() -> Dict[str, Any]:
    with LOCK:
        raw = read_json(ACCOUNTS_PATH, None)
        if not isinstance(raw, dict):
            raw = default_accounts_payload()
            atomic_write_json(ACCOUNTS_PATH, raw)
        return normalize_accounts(raw)


def normalize_accounts(raw: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(raw or {})
    profiles_raw = data.get("profiles")
    profiles: Dict[str, Dict[str, Any]] = {}

    if isinstance(profiles_raw, dict):
        iterable = profiles_raw.items()
    elif isinstance(profiles_raw, list):
        iterable = []
        for item in profiles_raw:
            if isinstance(item, dict):
                key = clean_text(item.get("id")) or clean_text(item.get("name"))
                iterable.append((key, item))
    else:
        iterable = []

    for key, item in iterable:
        if not isinstance(item, dict):
            continue
        profile = dict(item)
        profile_id = clean_text(profile.get("id")) or clean_text(key)
        if not profile_id:
            continue
        profile["id"] = profile_id
        profile.setdefault("name", profile.get("label") or profile_id)
        profile.setdefault("label", profile["name"])
        profile.setdefault("owner", "BEM FEB UKRIDA")
        profile.setdefault("role", "")
        profile.setdefault("plan", "Google AI Pro")
        profile.setdefault("provider", "google-antigravity")
        profile.setdefault("config_path", f"~/.config/antigravity-profiles/{profile_id}")
        profile.setdefault("status", "standby")
        profile.setdefault("enabled", True)
        profile.setdefault("hand_me_down", False)
        profile.setdefault("notes", "")
        profile.setdefault("created_at", data.get("updated_at") or now_iso())
        profile.setdefault("last_switched_at", None)
        profile.setdefault("switch_count", 0)
        profiles[profile_id] = profile

    if not profiles:
        fallback = default_accounts_payload()
        return normalize_accounts(fallback)

    active = clean_text(data.get("active_profile"))
    if active not in profiles:
        active = next(iter(profiles.keys()))

    data["profiles"] = profiles
    data["active_profile"] = active
    data.setdefault("default_model", DEFAULT_MODEL)
    data.setdefault("organization", ORGANIZATION)
    data.setdefault("schema_version", 1)
    data.setdefault("updated_at", now_iso())

    for profile_id, profile in profiles.items():
        if profile_id == active:
            profile["status"] = "active"
        elif profile.get("status") == "active":
            profile["status"] = "standby"
    return data


def accounts_as_list(accounts: Dict[str, Any]) -> List[Dict[str, Any]]:
    items = list(accounts.get("profiles", {}).values())
    active = accounts.get("active_profile")
    items.sort(
        key=lambda item: (
            0 if item.get("id") == active else 1,
            0 if not item.get("hand_me_down") else 1,
            str(item.get("id", "")),
        )
    )
    serialized: List[Dict[str, Any]] = []
    for item in items:
        profile = dict(item)
        config_path = expand_path(profile.get("config_path", ""))
        profile["config_path_resolved"] = str(config_path)
        profile["config_exists"] = bool(config_path and config_path.exists())
        serialized.append(profile)
    return serialized


def expand_path(value: Any) -> Optional[Path]:
    raw = clean_text(value)
    if not raw:
        return None
    return Path(os.path.expandvars(os.path.expanduser(raw)))


def get_active_profile(accounts: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    accounts = accounts or load_accounts()
    active_id = accounts.get("active_profile")
    profiles = accounts.get("profiles", {})
    if active_id not in profiles:
        active_id = next(iter(profiles.keys()))
    profile = dict(profiles[active_id])
    config_path = expand_path(profile.get("config_path"))
    profile["config_path_resolved"] = str(config_path) if config_path else ""
    profile["config_exists"] = bool(config_path and config_path.exists())
    return profile


def switch_profile(profile_id: str) -> Dict[str, Any]:
    target = clean_text(profile_id)
    if not target:
        raise ValueError("profile_id wajib diisi")

    with LOCK:
        accounts = load_accounts()
        profiles = accounts.get("profiles", {})
        if target not in profiles:
            available = ", ".join(sorted(profiles.keys()))
            raise KeyError(
                f"Profil '{target}' tidak ditemukan. Profil tersedia: {available}"
            )
        target_profile = profiles[target]
        if not target_profile.get("enabled", True):
            raise ValueError(f"Profil '{target}' sedang dinonaktifkan")

        old_active = accounts.get("active_profile")
        stamp = now_iso()
        for pid, profile in profiles.items():
            if pid == target:
                profile["status"] = "active"
                profile["last_switched_at"] = stamp
                profile["switch_count"] = safe_int(profile.get("switch_count"), 0) + 1
            else:
                profile["status"] = "standby"

        accounts["active_profile"] = target
        accounts["updated_at"] = stamp
        atomic_write_json(ACCOUNTS_PATH, accounts)

    log(f"[AKUN] Profil Antigravity aktif: {old_active} -> {target}")
    return {
        "previous_profile": old_active,
        "active_profile": target,
        "profile": get_active_profile(accounts),
        "accounts": accounts_as_list(accounts),
        "switched_at": stamp,
    }


# ---------------------------------------------------------------------------
# Data rapat, reminder, dan kalender ICS
# ---------------------------------------------------------------------------


def empty_meetings_payload() -> Dict[str, Any]:
    return {
        "schema_version": 1,
        "organization": ORGANIZATION,
        "updated_at": now_iso(),
        "meetings": [],
        "reminders": [],
    }


def load_meetings() -> Dict[str, Any]:
    with LOCK:
        raw = read_json(MEETINGS_PATH, None)
        if isinstance(raw, list):
            data = empty_meetings_payload()
            data["meetings"] = [item for item in raw if isinstance(item, dict)]
        elif isinstance(raw, dict):
            data = dict(raw)
            if not isinstance(data.get("meetings"), list):
                data["meetings"] = data.get("rapat") if isinstance(data.get("rapat"), list) else []
            if not isinstance(data.get("reminders"), list):
                data["reminders"] = []
        else:
            data = empty_meetings_payload()

        data["meetings"] = [item for item in data["meetings"] if isinstance(item, dict)]
        data["reminders"] = [
            item for item in data["reminders"] if isinstance(item, dict)
        ]
        data.setdefault("schema_version", 1)
        data.setdefault("organization", ORGANIZATION)
        data.setdefault("updated_at", now_iso())
        return data


def save_meetings(data: Dict[str, Any]) -> None:
    data["updated_at"] = now_iso()
    data["meetings"] = sorted(
        data.get("meetings", []),
        key=lambda item: (
            str(item.get("tanggal", "")),
            str(item.get("waktu", "")),
            str(item.get("created_at", "")),
        ),
    )
    data["reminders"] = sorted(
        data.get("reminders", []),
        key=lambda item: (
            str(item.get("tanggal", "")),
            str(item.get("waktu", "")),
            str(item.get("created_at", "")),
        ),
    )
    atomic_write_json(MEETINGS_PATH, data)


def add_meeting(payload: Dict[str, Any], source: str = "api") -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload rapat harus berupa objek JSON")

    agenda = clean_text(
        payload.get("agenda")
        or payload.get("deskripsi")
        or payload.get("description")
        or payload.get("keterangan")
    )
    judul = clean_text(
        payload.get("judul")
        or payload.get("title")
        or payload.get("nama")
        or payload.get("topik")
    )
    if not judul:
        judul = derive_title(agenda or payload.get("catatan", ""), "Rapat BEM FEB UKRIDA")
    if not agenda:
        agenda = clean_text(payload.get("catatan") or judul)

    raw_time = clean_text(
        payload.get("waktu")
        or payload.get("waktu_teks")
        or payload.get("time")
        or payload.get("jam")
    )
    raw_date = clean_text(
        payload.get("tanggal") or payload.get("date") or payload.get("hari")
    )

    default_date: Optional[date] = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date):
        try:
            default_date = date.fromisoformat(raw_date)
        except ValueError:
            default_date = None

    if raw_date and raw_time:
        schedule_source = f"{raw_date} {raw_time}"
    elif raw_date:
        schedule_source = raw_date
    else:
        schedule_source = raw_time
    schedule = parse_schedule(schedule_source, default_date=default_date)

    tempat = clean_text(
        payload.get("tempat")
        or payload.get("lokasi")
        or payload.get("location")
        or payload.get("place")
    )
    kategori = clean_text(payload.get("kategori") or payload.get("category"))
    if not kategori:
        kategori = "Rapat & Evaluasi"

    record = {
        "id": clean_text(payload.get("id")) or unique_id("mtg"),
        "judul": judul,
        "agenda": agenda,
        "deskripsi": clean_text(payload.get("deskripsi")) or agenda,
        "tanggal": schedule["tanggal"],
        "waktu": schedule["waktu"],
        "waktu_teks": schedule["waktu_teks"],
        "start_at": schedule["start_at"],
        "end_at": schedule["end_at"],
        "tempat": tempat or "Lokasi menyusul",
        "lokasi": tempat or "Lokasi menyusul",
        "kategori": kategori,
        "pj": clean_text(payload.get("pj") or payload.get("penanggung_jawab"))
        or "Arthur Reezan (Ketua BEM FEB)",
        "status": clean_text(payload.get("status")) or "Mendatang",
        "source": clean_text(payload.get("source")) or source,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    with LOCK:
        data = load_meetings()
        data["meetings"].append(record)
        save_meetings(data)
        generate_calendar(data)

    log(f"[RAPAT] {record['judul']} — {record['tanggal']} {record['waktu']}")
    return record


def add_reminder(payload: Dict[str, Any], source: str = "api") -> Dict[str, Any]:
    if not isinstance(payload, dict):
        raise ValueError("Payload reminder harus berupa objek JSON")

    isi = clean_text(
        payload.get("isi")
        or payload.get("reminder")
        or payload.get("text")
        or payload.get("judul")
    )
    if not isi:
        raise ValueError("Isi reminder wajib diisi")

    raw_time = clean_text(
        payload.get("waktu")
        or payload.get("waktu_teks")
        or payload.get("time")
        or payload.get("jam")
    )
    raw_date = clean_text(
        payload.get("tanggal") or payload.get("date") or payload.get("hari")
    )
    default_date: Optional[date] = None
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", raw_date):
        try:
            default_date = date.fromisoformat(raw_date)
        except ValueError:
            default_date = None

    if raw_date and raw_time:
        schedule_source = f"{raw_date} {raw_time}"
    elif raw_date:
        schedule_source = raw_date
    else:
        schedule_source = raw_time
    schedule = parse_schedule(schedule_source, default_date=default_date)

    record = {
        "id": clean_text(payload.get("id")) or unique_id("rmd"),
        "judul": clean_text(payload.get("judul")) or f"Reminder: {truncate(isi, 80)}",
        "isi": isi,
        "tanggal": schedule["tanggal"],
        "waktu": schedule["waktu"],
        "waktu_teks": schedule["waktu_teks"],
        "start_at": schedule["start_at"],
        "end_at": schedule["end_at"],
        "kategori": clean_text(payload.get("kategori")) or "Reminder",
        "pj": clean_text(payload.get("pj")) or "Arthur Reezan (Ketua BEM FEB)",
        "status": clean_text(payload.get("status")) or "Aktif",
        "source": clean_text(payload.get("source")) or source,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }

    with LOCK:
        data = load_meetings()
        data["reminders"].append(record)
        save_meetings(data)
        generate_calendar(data)

    log(f"[REMINDER] {record['isi']} — {record['tanggal']} {record['waktu']}")
    return record


def combined_events(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    for item in data.get("meetings", []):
        event = dict(item)
        event["type"] = "rapat"
        events.append(event)
    for item in data.get("reminders", []):
        event = dict(item)
        event["type"] = "reminder"
        event.setdefault("judul", item.get("isi", "Reminder"))
        events.append(event)
    events.sort(
        key=lambda item: (
            str(item.get("tanggal", "")),
            str(item.get("start_at") or item.get("waktu", "")),
        )
    )
    return events


def _ics_escape(value: Any) -> str:
    text = clean_text(value)
    text = text.replace("\\", "\\\\")
    text = text.replace(";", "\\;")
    text = text.replace(",", "\\,")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\n", "\\n")
    return text


def _ics_fold(line: str) -> str:
    if len(line) <= 74:
        return line
    parts = [line[:74]]
    remaining = line[74:]
    while remaining:
        parts.append(" " + remaining[:73])
        remaining = remaining[73:]
    return "\r\n".join(parts)


def _ics_datetime(value: Optional[str], fallback_date: str = "") -> Optional[datetime]:
    if value:
        try:
            parsed = datetime.fromisoformat(value)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=now_local().tzinfo)
            return parsed
        except ValueError:
            pass
    if fallback_date:
        try:
            return datetime.combine(
                date.fromisoformat(fallback_date), dt_time(0, 0)
            ).replace(tzinfo=now_local().tzinfo)
        except ValueError:
            return None
    return None


def generate_calendar(data: Optional[Dict[str, Any]] = None) -> str:
    data = data or load_meetings()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    lines: List[str] = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//BEM FEB UKRIDA//LK-FEB Bridge//ID",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH",
        "X-WR-CALNAME:BEM FEB UKRIDA — Rapat & Reminder",
        "X-WR-CALDESC:Kalender resmi BEM FEB UKRIDA dari LK-FEB Bridge",
        "X-WR-TIMEZONE:Asia/Jakarta",
    ]

    for event in combined_events(data):
        event_type = event.get("type", "rapat")
        start = _ics_datetime(
            event.get("start_at"), fallback_date=str(event.get("tanggal", ""))
        )
        end = _ics_datetime(
            event.get("end_at"), fallback_date=str(event.get("tanggal", ""))
        )
        if start is None:
            continue

        lines.append("BEGIN:VEVENT")
        uid = clean_text(event.get("id")) or unique_id("evt")
        lines.append(f"UID:{_ics_escape(uid)}@lk-feb.bem.ac.id")
        lines.append(f"DTSTAMP:{stamp}")
        lines.append(f"CREATED:{stamp}")
        lines.append(f"LAST-MODIFIED:{stamp}")

        if event.get("start_at"):
            lines.append(f"DTSTART:{start.strftime('%Y%m%dT%H%M%S')}")
            if end is None or end <= start:
                end = start + timedelta(hours=1)
            lines.append(f"DTEND:{end.strftime('%Y%m%dT%H%M%S')}")
        else:
            lines.append(f"DTSTART;VALUE=DATE:{start.strftime('%Y%m%d')}")
            lines.append(
                f"DTEND;VALUE=DATE:{(start + timedelta(days=1)).strftime('%Y%m%d')}"
            )

        if event_type == "reminder":
            summary = event.get("judul") or f"Reminder: {event.get('isi', '')}"
            description = event.get("isi", "")
            category = "REMINDER"
        else:
            summary = event.get("judul") or "Rapat BEM FEB UKRIDA"
            description = (
                f"Agenda: {event.get('agenda', '')}\n"
                f"PJ: {event.get('pj', '')}\n"
                f"Sumber: {event.get('source', 'LK-FEB Bridge')}"
            )
            category = event.get("kategori", "Rapat & Evaluasi")

        lines.append(f"SUMMARY:{_ics_escape(summary)}")
        lines.append(f"DESCRIPTION:{_ics_escape(description)}")
        lines.append(
            f"LOCATION:{_ics_escape(event.get('tempat') or event.get('lokasi') or '')}"
        )
        lines.append(f"CATEGORIES:{_ics_escape(category)}")
        lines.append(f"X-LK-FEB-TYPE:{event_type.upper()}")
        lines.append("STATUS:CONFIRMED")
        lines.append("TRANSP:OPAQUE")

        if event_type == "reminder" and event.get("start_at"):
            lines.append("BEGIN:VALARM")
            lines.append("TRIGGER:-PT15M")
            lines.append("ACTION:DISPLAY")
            lines.append(f"DESCRIPTION:{_ics_escape(summary)}")
            lines.append("END:VALARM")

        lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    content = "\r\n".join(_ics_fold(line) for line in lines) + "\r\n"
    atomic_write_text(CALENDAR_PATH, content)
    return str(CALENDAR_PATH)


# ---------------------------------------------------------------------------
# Notulensi (07_Second_Brain/notulensi)
# ---------------------------------------------------------------------------


def strip_code_fences(text: str) -> str:
    output = clean_text(text)
    output = re.sub(r"^\s*```[a-zA-Z0-9_-]*\s*\n", "", output)
    output = re.sub(r"\n```\s*$", "", output)
    output = re.sub(r"\x1b\[[0-9;]*[A-Za-z]", "", output)
    return output.strip()


def split_front_matter(text: str) -> Tuple[Dict[str, str], str]:
    content = text.lstrip("\ufeff")
    if not content.startswith("---"):
        return {}, content

    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, content

    closing = None
    for index in range(1, min(len(lines), 80)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return {}, content

    metadata: Dict[str, str] = {}
    for line in lines[1:closing]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('"') and value.endswith('"'):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                value = value[1:-1]
        elif value.startswith("'") and value.endswith("'"):
            value = value[1:-1]
        metadata[key] = value

    body = "\n".join(lines[closing + 1 :]).lstrip("\n")
    return metadata, body


def slugify(value: str, fallback: str = "notulensi") -> str:
    text = clean_text(value).lower()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-{2,}", "-", text).strip("-")
    return (text[:60] or fallback).strip("-")


def notulensi_item_from_path(
    path: Path, include_content: bool = False
) -> Optional[Dict[str, Any]]:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        stat = path.stat()
    except OSError:
        return None

    metadata, body = split_front_matter(content)
    title = metadata.get("judul") or ""
    if not title:
        for line in body.splitlines():
            if line.startswith("#"):
                title = line.lstrip("#").strip()
                if title:
                    break
    if not title:
        title = path.stem.replace("_", " ").replace("-", " ").strip()

    filename_date = ""
    match = re.match(r"^(\d{4}-\d{2}-\d{2})", path.name)
    if match:
        filename_date = match.group(1)

    excerpt = re.sub(r"\s+", " ", body).strip()
    item: Dict[str, Any] = {
        "id": metadata.get("id") or path.stem,
        "judul": title,
        "tanggal": metadata.get("tanggal") or filename_date,
        "waktu": metadata.get("waktu", ""),
        "tempat": metadata.get("tempat", ""),
        "rapat_id": metadata.get("rapat_id", ""),
        "sumber": metadata.get("sumber", "manual"),
        "dibuat": metadata.get("dibuat")
        or datetime.fromtimestamp(stat.st_mtime).astimezone().isoformat(timespec="seconds"),
        "filename": path.name,
        "path": str(path),
        "relative_path": str(path.relative_to(ROOT_DIR))
        if path.is_relative_to(ROOT_DIR)
        else str(path),
        "size_bytes": stat.st_size,
        "excerpt": truncate(excerpt, 280),
    }
    if include_content:
        item["content"] = body
    return item


def list_notulensi(
    include_content: bool = False, query: str = "", limit: int = 100
) -> Dict[str, Any]:
    ensure_dirs()
    files = sorted(
        [
            item
            for item in NOTULENSI_DIR.glob("*.md")
            if item.is_file() and not item.name.startswith(".")
        ],
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )

    all_items: List[Dict[str, Any]] = []
    for path in files:
        item = notulensi_item_from_path(path, include_content=include_content)
        if item:
            all_items.append(item)

    total = len(all_items)
    if query:
        needle = query.lower()
        all_items = [
            item
            for item in all_items
            if needle in str(item.get("judul", "")).lower()
            or needle in str(item.get("excerpt", "")).lower()
            or needle in str(item.get("content", "")).lower()
        ]

    limit = max(1, min(int(limit or 100), 500))
    return {
        "items": all_items[:limit],
        "total": total,
        "matched": len(all_items),
        "returned": min(len(all_items), limit),
    }


def build_mom_prompt(raw_text: str, metadata: Dict[str, str]) -> str:
    metadata_lines = "\n".join(
        f"- {key}: {metadata.get(key) or '—'}"
        for key in ("judul", "tanggal", "waktu", "tempat", "pimpinan", "notulis", "peserta")
    )
    return f"""Anda adalah Sekretaris Digital BEM FEB UKRIDA (Badan Eksekutif Mahasiswa Fakultas Ekonomi dan Bisnis, Universitas Kristen Krida Wacana).

TUGAS:
Ubah catatan mentah rapat berikut menjadi NOTULENSI RAPAT (Minutes of Meeting) resmi BEM FEB UKRIDA yang rapi, profesional, dan siap diarsipkan.

METADATA YANG TERSEDIA:
{metadata_lines}

CATATAN MENTAH DARI KETUA BEM:
---
{raw_text}
---

ATURAN:
1. Jangan mengarang fakta, angka, nama, atau keputusan yang tidak ada di catatan. Jika informasi tidak tersedia, tulis "—" atau "Belum ditentukan".
2. Pertahankan seluruh substansi catatan. Rapikan bahasa menjadi bahasa Indonesia baku dan formal.
3. Gunakan struktur berikut:
   # NOTULENSI RAPAT — <judul>
   ## I. INFORMASI UMUM
   (tabel: Hari/Tanggal, Waktu, Tempat, Pimpinan Rapat, Notulis, Peserta)
   ## II. AGENDA RAPAT
   ## III. PEMBAHASAN
   (poin-poin terstruktur per agenda)
   ## IV. KEPUTUSAN RAPAT
   ## V. RENCANA TINDAK LANJUT (ACTION ITEMS)
   (tabel: No | Kegiatan | PIC | Tenggat | Status)
   ## VI. CATATAN TAMBAHAN
   ## VII. PENUTUP
4. Sertakan kop identitas ringkas di awal dokumen: "BEM FEB UKRIDA — Fakultas Ekonomi dan Bisnis — Universitas Kristen Krida Wacana".
5. Akhiri dengan blok tanda tangan:
   Mengetahui,
   Ketua BEM FEB UKRIDA

   Arthur Reezan
   NIM. 312023002
6. Keluarkan HANYA dokumen Markdown final. Jangan menambahkan penjelasan, pembuka, atau blok kode ```.
"""


def build_mom_fallback(raw_text: str, metadata: Dict[str, str]) -> str:
    title = metadata.get("judul") or derive_title(raw_text, "Rapat BEM FEB UKRIDA")
    rows = [
        ("Hari/Tanggal", format_tanggal_indonesia(metadata.get("tanggal", ""))),
        ("Waktu", metadata.get("waktu") or "—"),
        ("Tempat", metadata.get("tempat") or "—"),
        ("Pimpinan Rapat", metadata.get("pimpinan") or "Arthur Reezan (Ketua BEM FEB)"),
        ("Notulis", metadata.get("notulis") or "Sekretaris Digital BEM FEB"),
        ("Peserta", metadata.get("peserta") or "—"),
    ]
    info_table = "\n".join(f"| {key} | {value} |" for key, value in rows)
    notes = clean_text(raw_text) or "_Tidak ada catatan mentah._"
    return f"""# NOTULENSI RAPAT — {title}

**BEM FEB UKRIDA — Fakultas Ekonomi dan Bisnis — Universitas Kristen Krida Wacana**

## I. INFORMASI UMUM

| Item | Keterangan |
|---|---|
{info_table}

## II. AGENDA RAPAT

{metadata.get("agenda") or title}

## III. PEMBAHASAN

{notes}

## IV. KEPUTUSAN RAPAT

_Belum ada keputusan yang dirumuskan secara eksplisit dalam catatan._

## V. RENCANA TINDAK LANJUT (ACTION ITEMS)

| No | Kegiatan | PIC | Tenggat | Status |
|---|---|---|---|---|
| 1 | Tindak lanjut hasil rapat | — | — | Belum ditentukan |

## VI. CATATAN TAMBAHAN

_Notulensi ini disusun otomatis dalam mode dasar karena mesin Antigravity belum tersedia. Seluruh catatan mentah dipertahankan pada Bagian III._

## VII. PENUTUP

Demikian notulensi rapat ini disusun sebagai dokumentasi resmi BEM FEB UKRIDA.

Mengetahui,
Ketua BEM FEB UKRIDA

Arthur Reezan
NIM. 312023002
"""


def save_notulensi(
    content: str,
    metadata: Optional[Dict[str, Any]] = None,
    source: str = "telegram",
    raw_text: str = "",
) -> Dict[str, Any]:
    ensure_dirs()
    metadata = dict(metadata or {})
    body = strip_code_fences(content or "")
    if not body:
        body = build_mom_fallback(raw_text, metadata)

    # Hindari front matter ganda dari model.
    _, body = split_front_matter(body)
    body = strip_code_fences(body)
    if not body.lstrip().startswith("#"):
        title = metadata.get("judul") or "Notulensi Rapat BEM FEB UKRIDA"
        body = f"# NOTULENSI RAPAT — {title}\n\n{body}"

    judul = clean_text(metadata.get("judul")) or derive_title(
        body, "Notulensi Rapat BEM FEB UKRIDA"
    )
    judul = re.sub(r"^#+\s*", "", judul).strip()
    if judul.upper().startswith("NOTULENSI RAPAT"):
        judul = re.sub(
            r"^NOTULENSI RAPAT\s*[—\-:]*\s*", "", judul, flags=re.IGNORECASE
        ).strip() or judul

    created = now_local()
    identifier = metadata.get("id") or unique_id("mom")
    filename = f"{created.strftime('%Y-%m-%d_%H%M%S')}_{slugify(judul)}.md"
    path = NOTULENSI_DIR / filename

    front_matter: Dict[str, str] = {
        "id": identifier,
        "judul": judul,
        "tanggal": clean_text(metadata.get("tanggal")) or created.date().isoformat(),
        "waktu": clean_text(metadata.get("waktu")) or created.strftime("%H:%M WIB"),
        "tempat": clean_text(metadata.get("tempat")),
        "rapat_id": clean_text(metadata.get("rapat_id")),
        "sumber": clean_text(metadata.get("sumber")) or source,
        "dibuat": created.isoformat(timespec="seconds"),
    }
    if metadata.get("pimpinan"):
        front_matter["pimpinan"] = clean_text(metadata.get("pimpinan"))
    if metadata.get("peserta"):
        front_matter["peserta"] = clean_text(metadata.get("peserta"))

    header_lines = ["---"]
    for key, value in front_matter.items():
        header_lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    header_lines.append("---")

    full_content = "\n".join(header_lines) + "\n\n" + body.rstrip() + "\n"
    atomic_write_text(path, full_content)
    log(f"[NOTULENSI] Tersimpan: {path}")

    item = notulensi_item_from_path(path, include_content=False) or {}
    item["absolute_path"] = str(path)
    return item


# ---------------------------------------------------------------------------
# Eksekusi Antigravity
# ---------------------------------------------------------------------------


def resolve_antigravity_bin() -> str:
    override = clean_text(os.environ.get("LK_FEB_ANTIGRAVITY_BIN"))
    if override:
        return override
    found = shutil.which("antigravity")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "antigravity"
    if fallback.exists():
        return str(fallback)
    return "antigravity"


def _terminate_process_tree(process: subprocess.Popen) -> None:
    try:
        if os.name == "posix":
            os.killpg(os.getpgid(process.pid), signal.SIGKILL)
        else:  # pragma: no cover - bridge berjalan di Linux
            process.kill()
    except (ProcessLookupError, PermissionError, OSError):
        try:
            process.kill()
        except OSError:
            pass


def run_antigravity(
    instruction: str,
    timeout: int = 300,
    model: str = DEFAULT_MODEL,
    dry_run: bool = False,
) -> Dict[str, Any]:
    instruction = clean_text(instruction)
    if not instruction:
        raise ValueError("Instruksi tidak boleh kosong")

    model = clean_text(model) or DEFAULT_MODEL
    timeout = max(5, min(safe_int(timeout, 300), 1800))
    binary = resolve_antigravity_bin()
    command = [
        binary,
        "run",
        instruction,
        "--model",
        model,
        "--auto",
    ]

    accounts = load_accounts()
    profile = get_active_profile(accounts)
    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")
    env["LK_FEB_ACTIVE_ANTIGRAVITY_PROFILE"] = str(profile.get("id", ""))
    env["LK_FEB_BRIDGE_DIR"] = str(BRIDGE_DIR)
    env["ANTIGRAVITY_PROFILE"] = str(profile.get("id", ""))
    env["ANTIGRAVITY_CONFIG_PATH"] = str(profile.get("config_path_resolved", ""))

    base_result: Dict[str, Any] = {
        "ok": False,
        "command": command,
        "command_display": shlex.join(command),
        "model": model,
        "profile": profile.get("id"),
        "profile_name": profile.get("name"),
        "cwd": str(ROOT_DIR),
        "timeout_seconds": timeout,
        "dry_run": dry_run,
    }

    if dry_run:
        base_result.update(
            {
                "ok": True,
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "output": "",
                "duration_seconds": 0,
            }
        )
        return base_result

    started = time.time()
    try:
        process = subprocess.Popen(
            command,
            cwd=str(ROOT_DIR),
            env=env,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            start_new_session=True,
        )
    except FileNotFoundError:
        base_result.update(
            {
                "error": (
                    "Perintah 'antigravity' tidak ditemukan. Pastikan wrapper "
                    "~/.local/bin/antigravity tersedia di PATH."
                ),
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "output": "",
                "duration_seconds": 0,
                "http_status": 503,
            }
        )
        return base_result
    except OSError as exc:
        base_result.update(
            {
                "error": f"Gagal menjalankan Antigravity: {exc}",
                "returncode": None,
                "stdout": "",
                "stderr": "",
                "output": "",
                "duration_seconds": 0,
                "http_status": 503,
            }
        )
        return base_result

    timed_out = False
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        _terminate_process_tree(process)
        try:
            stdout, stderr = process.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            stdout, stderr = "", ""

    duration = round(time.time() - started, 2)
    stdout = stdout or ""
    stderr = stderr or ""
    returncode = process.returncode

    output = strip_code_fences(stdout) or strip_code_fences(stderr)
    truncated_stdout = len(stdout) > 200_000
    truncated_stderr = len(stderr) > 50_000

    result = dict(base_result)
    result.update(
        {
            "ok": (not timed_out and returncode == 0),
            "returncode": returncode,
            "stdout": stdout[:200_000],
            "stderr": stderr[:50_000],
            "stdout_truncated": truncated_stdout,
            "stderr_truncated": truncated_stderr,
            "output": output[:200_000],
            "duration_seconds": duration,
            "timed_out": timed_out,
        }
    )
    if timed_out:
        result["error"] = f"Antigravity melewati batas waktu {timeout} detik."
        result["http_status"] = 504
    elif returncode != 0:
        result["error"] = (
            f"Antigravity keluar dengan kode {returncode}. "
            f"{truncate(stderr or stdout, 400)}"
        )
    else:
        result["http_status"] = 200
    return result


# ---------------------------------------------------------------------------
# Status sistem
# ---------------------------------------------------------------------------


def telegram_status_snapshot() -> Dict[str, Any]:
    config = read_json(TELEGRAM_CONFIG_PATH, {})
    token = clean_text(
        os.environ.get("LK_FEB_TELEGRAM_BOT_TOKEN") or config.get("bot_token", "")
    )
    token_configured = bool(token and "YOUR_" not in token and token != "PASTE_TOKEN_HERE")
    state = read_json(TELEGRAM_STATUS_PATH, {})
    if not isinstance(state, dict):
        state = {}

    heartbeat = clean_text(state.get("last_poll") or state.get("heartbeat") or "")
    age_seconds: Optional[float] = None
    if heartbeat:
        try:
            parsed = datetime.fromisoformat(heartbeat)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=now_local().tzinfo)
            age_seconds = max(0.0, (now_local() - parsed).total_seconds())
        except ValueError:
            age_seconds = None

    pid = state.get("pid")
    alive = pid_is_alive(pid) if pid else False
    status = clean_text(state.get("status")) or "offline"
    online = (
        status == "online"
        and age_seconds is not None
        and age_seconds <= 120
        and (alive or pid in (None, ""))
    )
    if status == "online" and not online:
        status = "offline"

    return {
        "configured": token_configured,
        "online": online,
        "status": "online" if online else status,
        "username": state.get("username"),
        "pid": pid,
        "process_alive": alive,
        "last_poll": heartbeat or None,
        "heartbeat_age_seconds": round(age_seconds, 1) if age_seconds is not None else None,
        "last_error": state.get("last_error"),
        "started_at": state.get("started_at"),
        "last_update_id": state.get("last_update_id"),
        "allowed_chat_count": len(config.get("allowed_chat_ids") or []),
        "token_configured": token_configured,
    }


def get_status() -> Dict[str, Any]:
    accounts = load_accounts()
    active = get_active_profile(accounts)
    data = load_meetings()
    notulensi = list_notulensi(include_content=False, limit=5)
    bot = telegram_status_snapshot()

    meetings = data.get("meetings", [])
    reminders = data.get("reminders", [])
    return {
        "ok": True,
        "service": "LK-FEB Bridge",
        "organization": ORGANIZATION,
        "address": CAMPUS_ADDRESS,
        "version": SERVER_VERSION,
        "time": now_iso(),
        "uptime_seconds": round(time.time() - STARTED_AT, 1),
        "server": {
            "host": HOST,
            "port": PORT,
            "base_url": f"http://{HOST}:{PORT}",
            "started_at": datetime.fromtimestamp(STARTED_AT)
            .astimezone()
            .isoformat(timespec="seconds"),
        },
        "active_profile": active.get("id"),
        "active_profile_id": active.get("id"),
        "active_account": active,
        "accounts": accounts_as_list(accounts),
        "profiles": accounts_as_list(accounts),
        "default_model": accounts.get("default_model", DEFAULT_MODEL),
        "telegram": bot,
        "telegram_bot": bot,
        "total_notulensi": notulensi["total"],
        "total_rapat": len(meetings),
        "total_reminders": len(reminders),
        "totals": {
            "notulensi": notulensi["total"],
            "rapat": len(meetings),
            "reminders": len(reminders),
            "meetings": len(meetings),
        },
        "latest_notulensi": notulensi["items"],
        "paths": {
            "bridge": str(BRIDGE_DIR),
            "data": str(DATA_DIR),
            "notulensi": str(NOTULENSI_DIR),
            "calendar": str(CALENDAR_PATH),
            "accounts": str(ACCOUNTS_PATH),
        },
        "calendar": {
            "path": str(CALENDAR_PATH),
            "exists": CALENDAR_PATH.exists(),
            "updated_at": datetime.fromtimestamp(CALENDAR_PATH.stat().st_mtime)
            .astimezone()
            .isoformat(timespec="seconds")
            if CALENDAR_PATH.exists()
            else None,
        },
    }


# ---------------------------------------------------------------------------
# File awal (idempotent)
# ---------------------------------------------------------------------------


def ensure_runtime_files() -> None:
    ensure_dirs()
    if not ACCOUNTS_PATH.exists():
        atomic_write_json(ACCOUNTS_PATH, default_accounts_payload())
    if not MEETINGS_PATH.exists():
        atomic_write_json(MEETINGS_PATH, empty_meetings_payload())
    if not TELEGRAM_CONFIG_PATH.exists():
        atomic_write_json(
            TELEGRAM_CONFIG_PATH,
            {
                "schema_version": 1,
                "bot_token": "",
                "allowed_chat_ids": [],
                "owner_name": "Arthur Reezan",
                "owner_title": "Ketua BEM FEB UKRIDA",
                "default_timezone": "Asia/Jakarta",
                "poll_timeout_seconds": 25,
                "notulensi_ai_timeout_seconds": 300,
                "notulensi_ai_enabled": True,
            },
        )
    if not CALENDAR_PATH.exists():
        try:
            generate_calendar(load_meetings())
        except Exception as exc:  # kalender bersifat best-effort
            log(f"[WARN] Gagal membuat kalender awal: {exc}")


# ---------------------------------------------------------------------------
# HTTP server
# ---------------------------------------------------------------------------


class BridgeRequestHandler(BaseHTTPRequestHandler):
    server_version = f"LK-FEB-Bridge/{SERVER_VERSION}"
    protocol_version = "HTTP/1.1"

    # ----- util response -------------------------------------------------
    def _cors_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type, Authorization, X-Requested-With, Accept, Origin",
        )
        self.send_header("Access-Control-Max-Age", "86400")
        self.send_header("Vary", "Origin")

    def _send_json(self, status_code: int, payload: Any) -> None:
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self._cors_headers()
            self.end_headers()
            self.wfile.write(body)
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _send_empty(self, status_code: int = 204) -> None:
        try:
            self.send_response(status_code)
            self.send_header("Content-Length", "0")
            self.send_header("Cache-Control", "no-store")
            self._cors_headers()
            self.end_headers()
        except (BrokenPipeError, ConnectionResetError):
            pass

    def _read_json_body(self) -> Dict[str, Any]:
        length_header = self.headers.get("Content-Length")
        if not length_header:
            raise ValueError("Body JSON diperlukan (Content-Length tidak ditemukan)")
        length = safe_int(length_header, 0)
        if length <= 0:
            raise ValueError("Body JSON kosong")
        if length > 2 * 1024 * 1024:
            raise ValueError("Body JSON terlalu besar (maksimum 2 MB)")
        raw = self.rfile.read(length)
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError(f"JSON tidak valid: {exc}") from exc
        if not isinstance(parsed, dict):
            raise ValueError("Body JSON harus berupa objek")
        return parsed

    def _query(self) -> Dict[str, List[str]]:
        return parse_qs(urlparse(self.path).query)

    def _route(self) -> str:
        path = urlparse(self.path).path
        if path != "/":
            path = path.rstrip("/")
        return path or "/"

    # ----- HTTP verbs ----------------------------------------------------
    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send_empty(204)

    def do_GET(self) -> None:  # noqa: N802
        try:
            route = self._route()
            if route in ("/", "/api"):
                self._send_json(
                    200,
                    {
                        "ok": True,
                        "service": "LK-FEB Bridge",
                        "version": SERVER_VERSION,
                        "organization": ORGANIZATION,
                        "endpoints": [
                            "GET /api/status",
                            "POST /api/antigravity/switch",
                            "POST /api/antigravity/run",
                            "GET /api/meetings",
                            "POST /api/meetings",
                            "GET /api/notulensi",
                            "OPTIONS *",
                        ],
                    },
                )
                return

            if route == "/health":
                self._send_json(
                    200,
                    {
                        "ok": True,
                        "status": "healthy",
                        "service": "LK-FEB Bridge",
                        "time": now_iso(),
                        "uptime_seconds": round(time.time() - STARTED_AT, 1),
                    },
                )
                return

            if route == "/api/status":
                self._send_json(200, get_status())
                return

            if route == "/api/meetings":
                data = load_meetings()
                events = combined_events(data)
                event_type = clean_text(
                    (self._query().get("type") or [""])[0]
                ).lower()
                meetings = data.get("meetings", [])
                reminders = data.get("reminders", [])
                if event_type in ("rapat", "meeting", "meetings"):
                    events = [item for item in events if item.get("type") == "rapat"]
                elif event_type in ("reminder", "reminders"):
                    events = [item for item in events if item.get("type") == "reminder"]

                self._send_json(
                    200,
                    {
                        "ok": True,
                        "meetings": meetings,
                        "rapat": meetings,
                        "reminders": reminders,
                        "events": events,
                        "total_meetings": len(meetings),
                        "total_rapat": len(meetings),
                        "total_reminders": len(reminders),
                        "total_events": len(events),
                        "updated_at": data.get("updated_at"),
                        "calendar": str(CALENDAR_PATH),
                    },
                )
                return

            if route == "/api/notulensi":
                query = self._query()
                include_content = (query.get("full") or ["0"])[0].lower() in (
                    "1",
                    "true",
                    "yes",
                )
                search = (query.get("q") or [""])[0]
                limit = safe_int((query.get("limit") or ["100"])[0], 100)
                result = list_notulensi(
                    include_content=include_content, query=search, limit=limit
                )
                self._send_json(
                    200,
                    {
                        "ok": True,
                        "notulensi": result["items"],
                        "items": result["items"],
                        "total": result["total"],
                        "total_notulensi": result["total"],
                        "matched": result["matched"],
                        "returned": result["returned"],
                        "directory": str(NOTULENSI_DIR),
                    },
                )
                return

            self._send_json(
                404,
                {
                    "ok": False,
                    "error": "Endpoint tidak ditemukan",
                    "method": "GET",
                    "path": route,
                },
            )
        except Exception as exc:
            log(f"[ERROR] GET {self.path}: {exc}")
            traceback.print_exc()
            self._send_json(
                500, {"ok": False, "error": f"Kesalahan server: {exc}"}
            )

    def do_POST(self) -> None:  # noqa: N802
        try:
            route = self._route()
            payload = self._read_json_body()

            if route == "/api/antigravity/switch":
                profile_id = clean_text(
                    payload.get("profile_id")
                    or payload.get("profile")
                    or payload.get("id")
                    or payload.get("akun")
                )
                try:
                    result = switch_profile(profile_id)
                except KeyError as exc:
                    self._send_json(404, {"ok": False, "error": str(exc).strip("'")})
                    return
                except ValueError as exc:
                    self._send_json(400, {"ok": False, "error": str(exc)})
                    return

                self._send_json(
                    200,
                    {
                        "ok": True,
                        "message": f"Akun Antigravity aktif: {result['active_profile']}",
                        **result,
                    },
                )
                return

            if route == "/api/antigravity/run":
                instruction = clean_text(
                    payload.get("instruction")
                    or payload.get("instruksi")
                    or payload.get("prompt")
                    or payload.get("message")
                    or payload.get("text")
                )
                if not instruction:
                    self._send_json(
                        400,
                        {
                            "ok": False,
                            "error": "Field 'instruction'/'instruksi' wajib diisi",
                        },
                    )
                    return

                timeout = safe_int(
                    payload.get("timeout") or payload.get("timeout_seconds"), 300
                )
                model = clean_text(payload.get("model")) or DEFAULT_MODEL
                dry_run = bool(payload.get("dry_run"))
                try:
                    result = run_antigravity(
                        instruction=instruction,
                        timeout=timeout,
                        model=model,
                        dry_run=dry_run,
                    )
                except ValueError as exc:
                    self._send_json(400, {"ok": False, "error": str(exc)})
                    return

                http_status = safe_int(result.pop("http_status", 200), 200)
                self._send_json(http_status, result)
                return

            if route == "/api/meetings":
                event_type = clean_text(
                    payload.get("type")
                    or payload.get("tipe")
                    or payload.get("jenis")
                ).lower()
                try:
                    if event_type in ("reminder", "pengingat"):
                        record = add_reminder(payload, source="api")
                        self._send_json(
                            201,
                            {
                                "ok": True,
                                "message": "Reminder berhasil disimpan",
                                "reminder": record,
                                "item": record,
                            },
                        )
                    else:
                        record = add_meeting(payload, source="api")
                        self._send_json(
                            201,
                            {
                                "ok": True,
                                "message": "Rapat berhasil ditambahkan",
                                "meeting": record,
                                "item": record,
                            },
                        )
                except ValueError as exc:
                    self._send_json(400, {"ok": False, "error": str(exc)})
                return

            self._send_json(
                404,
                {
                    "ok": False,
                    "error": "Endpoint tidak ditemukan",
                    "method": "POST",
                    "path": route,
                },
            )
        except ValueError as exc:
            self._send_json(400, {"ok": False, "error": str(exc)})
        except Exception as exc:
            log(f"[ERROR] POST {self.path}: {exc}")
            traceback.print_exc()
            self._send_json(
                500, {"ok": False, "error": f"Kesalahan server: {exc}"}
            )

    def log_message(self, fmt: str, *args: Any) -> None:
        log(f"[HTTP] {self.address_string()} {fmt % args}")


def create_server(host: str = HOST, port: int = PORT) -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((host, port), BridgeRequestHandler)
    httpd.daemon_threads = True
    httpd.allow_reuse_address = True
    with SERVER_STATE_LOCK:
        SERVER_STATE["server"] = httpd
    return httpd


def shutdown_server() -> None:
    with SERVER_STATE_LOCK:
        httpd = SERVER_STATE.get("server")
    if httpd is None:
        return

    def _shutdown() -> None:
        try:
            httpd.shutdown()
        except Exception:
            pass

    threading.Thread(target=_shutdown, name="bridge-shutdown", daemon=True).start()


def run_server(
    host: str = HOST,
    port: int = PORT,
    stop_event: Optional[threading.Event] = None,
) -> None:
    global HOST, PORT
    HOST = host
    PORT = port
    ensure_runtime_files()

    httpd = create_server(host, port)
    log("=" * 68)
    log("  LK-FEB BRIDGE SERVER — BEM FEB UKRIDA")
    log(f"  HTTP API : http://{host}:{port}")
    log(f"  Data     : {DATA_DIR}")
    log(f"  Notulensi: {NOTULENSI_DIR}")
    log(f"  Kalender : {CALENDAR_PATH}")
    log("=" * 68)

    if stop_event is None:
        try:
            httpd.serve_forever(poll_interval=0.5)
        except KeyboardInterrupt:
            log("[SERVER] Dihentikan oleh pengguna.")
        finally:
            httpd.server_close()
            with SERVER_STATE_LOCK:
                SERVER_STATE.pop("server", None)
        return

    httpd.timeout = 0.5
    try:
        while not stop_event.is_set():
            httpd.handle_request()
    finally:
        httpd.server_close()
        with SERVER_STATE_LOCK:
            SERVER_STATE.pop("server", None)
        log("[SERVER] HTTP server berhenti.")


def main() -> int:
    parser = argparse.ArgumentParser(description="LK-FEB Bridge Server (BEM FEB UKRIDA)")
    parser.add_argument(
        "--host",
        default=HOST,
        help=f"Alamat bind HTTP (default: {HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=PORT,
        help=f"Port HTTP (default: {PORT})",
    )
    args = parser.parse_args()
    run_server(args.host, args.port)
    return 0


if __name__ == "__main__":
    sys.exit(main())
