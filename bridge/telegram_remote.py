#!/usr/bin/env python3
"""
LK-FEB TELEGRAM EXECUTIVE REMOTE
================================
Bot Telegram mandiri untuk Ketua BEM FEB UKRIDA.

Menggunakan HTTP polling langsung ke Bot API Telegram melalui urllib.request
(tanpa library pihak ketiga). Semua data ditulis ke Bridge LK-FEB sehingga
otomatis tampil di Portal LK-FEB.

Perintah:
  /start, /help        Status sistem & menu
  /rapat               waktu | tempat | agenda
  /reminder            waktu | isi
  /akun                Daftar akun Antigravity
  /akun_switch <id>    Ganti akun Antigravity aktif
  /notulensi [kata]    Notulensi terbaru
  /status              Status ringkas
  /id                  Chat ID Telegram

Teks bebas akan diubah menjadi Minutes of Meeting resmi BEM FEB UKRIDA
menggunakan Antigravity DeepSeek, lalu disimpan ke 07_Second_Brain/notulensi/.
"""

from __future__ import annotations

import json
import os
import re
import signal
import sys
import threading
import time
import urllib.error
import urllib.request
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

BRIDGE_DIR = Path(__file__).resolve().parent
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

import bridge_server as bridge  # noqa: E402

API_ROOT = "https://api.telegram.org"
MAX_MESSAGE_LENGTH = 3900

DEFAULT_COMMANDS = [
    {"command": "start", "description": "Status sistem BEM FEB & menu perintah"},
    {"command": "rapat", "description": "Catat rapat: /rapat waktu | tempat | agenda"},
    {"command": "reminder", "description": "Simpan reminder: /reminder waktu | isi"},
    {"command": "akun", "description": "Lihat akun Antigravity & statusnya"},
    {"command": "akun_switch", "description": "Ganti akun: /akun_switch <id>"},
    {"command": "notulensi", "description": "Lihat notulensi terbaru"},
    {"command": "status", "description": "Status ringkas sistem bridge"},
]


# ---------------------------------------------------------------------------
# Klien Bot API
# ---------------------------------------------------------------------------


class TelegramError(Exception):
    def __init__(
        self,
        description: str,
        error_code: Optional[int] = None,
        retry_after: Optional[int] = None,
    ) -> None:
        super().__init__(description)
        self.description = description
        self.error_code = error_code
        self.retry_after = retry_after


class TelegramClient:
    def __init__(self, token: str, user_agent: str = "LK-FEB-Bridge/1.0") -> None:
        self.token = token
        self.user_agent = user_agent

    def _call(
        self,
        method: str,
        payload: Optional[Dict[str, Any]] = None,
        timeout: float = 35.0,
    ) -> Any:
        url = f"{API_ROOT}/bot{self.token}/{method}"
        data = json.dumps(payload or {}, ensure_ascii=False).encode("utf-8")
        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json; charset=utf-8",
                "User-Agent": self.user_agent,
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = response.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            raw = exc.read().decode("utf-8", errors="replace")
            description = f"HTTP {exc.code}"
            error_code = exc.code
            retry_after = None
            try:
                parsed = json.loads(raw)
                description = parsed.get("description") or description
                error_code = parsed.get("error_code", error_code)
                parameters = parsed.get("parameters") or {}
                retry_after = parameters.get("retry_after")
            except (json.JSONDecodeError, AttributeError):
                pass
            raise TelegramError(description, error_code, retry_after) from exc
        except urllib.error.URLError as exc:
            raise TelegramError(f"Koneksi ke Telegram gagal: {exc.reason}") from exc
        except TimeoutError as exc:
            raise TelegramError("Koneksi ke Telegram timeout") from exc

        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise TelegramError("Respons Telegram bukan JSON yang valid") from exc

        if not parsed.get("ok"):
            parameters = parsed.get("parameters") or {}
            raise TelegramError(
                parsed.get("description") or "Permintaan Telegram gagal",
                parsed.get("error_code"),
                parameters.get("retry_after"),
            )
        return parsed.get("result")

    def get_me(self) -> Dict[str, Any]:
        return self._call("getMe", timeout=20)

    def get_updates(
        self,
        offset: int = 0,
        timeout: int = 25,
        allowed_updates: Optional[List[str]] = None,
    ) -> List[Dict[str, Any]]:
        payload: Dict[str, Any] = {
            "timeout": max(0, min(int(timeout), 50)),
            "allowed_updates": allowed_updates or ["message"],
        }
        if offset:
            payload["offset"] = int(offset)
        result = self._call("getUpdates", payload, timeout=timeout + 15)
        return result if isinstance(result, list) else []

    def send_message(
        self,
        chat_id: Any,
        text: str,
        markdown: bool = True,
        reply_markup: Optional[Dict[str, Any]] = None,
    ) -> None:
        chunks = split_message(text, MAX_MESSAGE_LENGTH)
        for index, chunk in enumerate(chunks):
            payload: Dict[str, Any] = {
                "chat_id": chat_id,
                "text": chunk,
                "disable_web_page_preview": True,
            }
            if markdown:
                payload["parse_mode"] = "Markdown"
            if reply_markup and index == 0:
                payload["reply_markup"] = reply_markup
            try:
                self._call("sendMessage", payload, timeout=30)
            except TelegramError as exc:
                # Jika Markdown pengguna/model merusak parse, kirim sebagai teks biasa.
                if markdown and exc.error_code == 400 and "parse" in exc.description.lower():
                    payload.pop("parse_mode", None)
                    self._call("sendMessage", payload, timeout=30)
                else:
                    raise

    def send_typing(self, chat_id: Any) -> None:
        try:
            self._call(
                "sendChatAction",
                {"chat_id": chat_id, "action": "typing"},
                timeout=10,
            )
        except TelegramError:
            pass

    def set_my_commands(self, commands: List[Dict[str, str]]) -> None:
        self._call("setMyCommands", {"commands": commands}, timeout=20)


def split_message(text: str, limit: int = MAX_MESSAGE_LENGTH) -> List[str]:
    text = str(text or "").strip()
    if not text:
        return []
    if len(text) <= limit:
        return [text]

    chunks: List[str] = []
    remaining = text
    while len(remaining) > limit:
        cut = remaining.rfind("\n", 0, limit)
        if cut < limit // 2:
            cut = remaining.rfind(" ", 0, limit)
        if cut < limit // 2:
            cut = limit
        chunks.append(remaining[:cut].rstrip())
        remaining = remaining[cut:].lstrip()
    if remaining:
        chunks.append(remaining)
    return chunks


# ---------------------------------------------------------------------------
# Konfigurasi
# ---------------------------------------------------------------------------


def load_config() -> Dict[str, Any]:
    raw = bridge.read_json(bridge.TELEGRAM_CONFIG_PATH, {})
    if not isinstance(raw, dict):
        raw = {}

    token = bridge.clean_text(
        os.environ.get("LK_FEB_TELEGRAM_BOT_TOKEN") or raw.get("bot_token")
    )
    ids = raw.get("allowed_chat_ids") or []
    if isinstance(ids, (int, float)):
        ids = [ids]
    elif isinstance(ids, str):
        ids = [part for part in re.split(r"[,;\s]+", ids) if part]
    elif not isinstance(ids, list):
        ids = []
    allowed_ids = {str(item).strip() for item in ids if str(item).strip()}

    usernames = raw.get("allowed_usernames") or []
    if isinstance(usernames, str):
        usernames = [item.strip().lstrip("@") for item in usernames.split(",")]
    if not isinstance(usernames, list):
        usernames = []
    allowed_usernames = {
        str(item).strip().lstrip("@").lower()
        for item in usernames
        if str(item).strip()
    }

    return {
        "raw": raw,
        "bot_token": token,
        "allowed_chat_ids": allowed_ids,
        "allowed_usernames": allowed_usernames,
        "owner_name": bridge.clean_text(raw.get("owner_name")) or "Arthur Reezan",
        "owner_title": bridge.clean_text(raw.get("owner_title"))
        or "Ketua BEM FEB UKRIDA",
        "poll_timeout": max(
            5, min(bridge.safe_int(raw.get("poll_timeout_seconds"), 25), 50)
        ),
        "notulensi_ai_timeout": max(
            30,
            min(
                bridge.safe_int(raw.get("notulensi_ai_timeout_seconds"), 300),
                900,
            ),
        ),
        "notulensi_ai_enabled": bool(raw.get("notulensi_ai_enabled", True)),
        "commands": raw.get("commands") or {},
    }


def token_looks_configured(token: str) -> bool:
    token = bridge.clean_text(token)
    return bool(
        token
        and "YOUR_" not in token
        and token != "PASTE_TOKEN_HERE"
        and re.match(r"^\d+:[A-Za-z0-9_-]{20,}$", token)
    )


# ---------------------------------------------------------------------------
# Bot
# ---------------------------------------------------------------------------


class TelegramBot:
    def __init__(self, stop_event: Optional[threading.Event] = None) -> None:
        self.stop_event = stop_event or threading.Event()
        self.config = load_config()
        self.client = TelegramClient(self.config["bot_token"])
        self.state_lock = threading.RLock()
        self.status_state: Dict[str, Any] = {
            "status": "offline",
            "pid": os.getpid(),
            "username": None,
            "last_poll": None,
            "last_error": "Belum berjalan",
            "started_at": bridge.now_iso(),
            "last_update_id": None,
            "allowed_chat_count": len(self.config["allowed_chat_ids"]),
        }
        self.offset = self._load_offset()
        self.heartbeat_thread: Optional[threading.Thread] = None

    # ----- status & offset ----------------------------------------------
    def _load_offset(self) -> int:
        payload = bridge.read_json(bridge.TELEGRAM_OFFSET_PATH, {})
        if isinstance(payload, dict):
            return bridge.safe_int(payload.get("offset"), 0)
        return 0

    def _save_offset(self, offset: int) -> None:
        try:
            bridge.atomic_write_json(
                bridge.TELEGRAM_OFFSET_PATH,
                {"offset": int(offset), "updated_at": bridge.now_iso()},
            )
        except OSError as exc:
            bridge.log(f"[TELEGRAM] Gagal menyimpan offset: {exc}")

    def _write_status(
        self,
        status: Optional[str] = None,
        error: Optional[str] = None,
    ) -> None:
        with self.state_lock:
            if status is not None:
                self.status_state["status"] = status
            if error is not None:
                self.status_state["last_error"] = error
            self.status_state["last_poll"] = bridge.now_iso()
            self.status_state["pid"] = os.getpid()
            self.status_state["allowed_chat_count"] = len(
                self.config["allowed_chat_ids"]
            )
            payload = dict(self.status_state)
        try:
            bridge.atomic_write_json(bridge.TELEGRAM_STATUS_PATH, payload)
        except OSError as exc:
            bridge.log(f"[TELEGRAM] Gagal menulis status: {exc}")

    def _heartbeat_loop(self) -> None:
        while not self.stop_event.is_set():
            self._write_status()
            self.stop_event.wait(15)

    # ----- akses ---------------------------------------------------------
    def _is_allowed(self, chat_id: str, message: Dict[str, Any]) -> bool:
        allowed_ids = self.config["allowed_chat_ids"]
        allowed_usernames = self.config["allowed_usernames"]
        if not allowed_ids and not allowed_usernames:
            return False
        if chat_id in allowed_ids:
            return True
        sender = message.get("from") or {}
        username = bridge.clean_text(sender.get("username")).lstrip("@").lower()
        return bool(username and username in allowed_usernames)

    # ----- format helpers -----------------------------------------------
    def _sender_name(self, message: Dict[str, Any]) -> str:
        sender = message.get("from") or {}
        name = " ".join(
            part
            for part in (
                bridge.clean_text(sender.get("first_name")),
                bridge.clean_text(sender.get("last_name")),
            )
            if part
        )
        return name or bridge.clean_text(sender.get("username")) or "Pengurus BEM FEB"

    def _sender_username(self, message: Dict[str, Any]) -> str:
        sender = message.get("from") or {}
        username = bridge.clean_text(sender.get("username"))
        return f"@{username}" if username else ""

    # ----- perintah ------------------------------------------------------
    def cmd_help(self, chat_id: str, message: Dict[str, Any]) -> None:
        status = bridge.get_status()
        active = status.get("active_account") or {}
        bot_status = "🟢 online" if status.get("telegram", {}).get("online") else "⚪ offline"
        owner_name = self.config["owner_name"]
        active_id = status.get("active_profile")
        active_name = active.get("name", "—")
        total_rapat = status.get("total_rapat", 0)
        total_reminders = status.get("total_reminders", 0)
        total_notulensi = status.get("total_notulensi", 0)
        text = f"""🏛️ *BEM FEB UKRIDA — EXECUTIVE REMOTE*
_Fakultas Ekonomi dan Bisnis — Universitas Kristen Krida Wacana_

👤 *Ketua BEM:* {owner_name}
🤖 *Akun Antigravity:* `{active_id}`
   {active_name}
📡 *Telegram Remote:* {bot_status}

📊 *RINGKASAN SISTEM*
• Rapat tercatat: *{total_rapat}*
• Reminder aktif: *{total_reminders}*
• Notulensi tersimpan: *{total_notulensi}*

🧭 *MENU PERINTAH*
/rapat `<waktu> | <tempat> | <agenda>`
/reminder `<waktu> | <isi>`
/akun — daftar akun Antigravity
/akun_switch `<id>` — pindah akun
/notulensi `[kata kunci]` — arsip MoM
/status — status ringkas
/id — lihat Chat ID Anda

💡 *Kirim catatan rapat biasa* (tanpa perintah), maka saya akan menyusunnya menjadi *Notulensi Resmi BEM FEB UKRIDA* dan menyimpannya ke Second Brain secara otomatis.

_Contoh:_
`/rapat Senin, 10 November 2026 16:00 | Ruang Rapat Lt. 3 | Rapat Pleno BPH`

_Semua data tersinkron ke Portal LK-FEB pada port 9440._"""
        self.client.send_message(chat_id, text)

    def cmd_status(self, chat_id: str, message: Dict[str, Any]) -> None:
        status = bridge.get_status()
        active = status.get("active_account") or {}
        telegram = status.get("telegram") or {}
        base_url = status.get("server", {}).get("base_url")
        active_id = status.get("active_profile")
        active_name = active.get("name", "—")
        bot_online = "online" if telegram.get("online") else "offline"
        total_rapat = status.get("total_rapat", 0)
        total_reminders = status.get("total_reminders", 0)
        total_notulensi = status.get("total_notulensi", 0)
        clock = bridge.now_local().strftime("%d/%m/%Y %H:%M WIB")
        text = f"""📡 *STATUS LK-FEB BRIDGE*

🟢 *Server:* `{base_url}`
🤖 *Akun Antigravity:* `{active_id}` — {active_name}
💬 *Telegram Bot:* {bot_online}

📅 Rapat: *{total_rapat}*
⏰ Reminder: *{total_reminders}*
📝 Notulensi: *{total_notulensi}*

🕒 {clock}"""
        self.client.send_message(chat_id, text)

    def cmd_id(self, chat_id: str, message: Dict[str, Any]) -> None:
        sender = self._sender_name(message)
        username = self._sender_username(message) or "—"
        text = f"""🪪 *IDENTITAS TELEGRAM*

• Chat ID: `{chat_id}`
• Nama: {sender}
• Username: {username}

Tambahkan Chat ID di atas ke `config/telegram_config.json` → `allowed_chat_ids` bila belum terdaftar."""
        self.client.send_message(chat_id, text)

    def cmd_rapat(self, chat_id: str, message: Dict[str, Any], args: str) -> None:
        args = bridge.clean_text(args)
        if not args:
            self.client.send_message(
                chat_id,
                "📅 *FORMAT PENCATATAN RAPAT*\n\n"
                "`/rapat <waktu> | <tempat> | <agenda>`\n\n"
                "Contoh:\n"
                "`/rapat Senin, 10 November 2026 16:00 | Ruang Rapat Lt. 3 | Rapat Pleno BPH`",
            )
            return

        parts = [part.strip() for part in args.split("|")]
        if len(parts) < 3:
            self.client.send_message(
                chat_id,
                "⚠️ Format belum lengkap. Gunakan pemisah `|`:\n\n"
                "`/rapat <waktu> | <tempat> | <agenda>`",
            )
            return

        waktu_raw = parts[0]
        tempat = parts[1]
        agenda = " | ".join(parts[2:]).strip()
        if not waktu_raw or not tempat or not agenda:
            self.client.send_message(
                chat_id,
                "⚠️ Waktu, tempat, dan agenda tidak boleh kosong.",
            )
            return

        schedule = bridge.parse_schedule(waktu_raw)
        sender = self._sender_name(message)
        payload = {
            "judul": bridge.derive_title(agenda, "Rapat BEM FEB UKRIDA"),
            "agenda": agenda,
            "deskripsi": agenda,
            "tanggal": schedule["tanggal"],
            "waktu": schedule["waktu"],
            "waktu_teks": waktu_raw,
            "tempat": tempat,
            "kategori": "Rapat & Evaluasi",
            "pj": sender,
            "status": "Mendatang",
            "source": "telegram",
        }

        try:
            record = bridge.add_meeting(payload, source="telegram")
        except Exception as exc:
            bridge.log(f"[TELEGRAM] Gagal menambah rapat: {exc}")
            self.client.send_message(
                chat_id, f"❌ *Gagal mencatat rapat*\n\n`{exc}`"
            )
            return

        record_title = record["judul"]
        record_date = bridge.format_tanggal_indonesia(record["tanggal"])
        record_time = record["waktu"]
        record_place = record["tempat"]
        record_pj = record["pj"]
        record_id = record["id"]
        record_agenda = record["agenda"]
        text = f"""✅ *RAPAT BERHASIL DICATAT*

📌 *{record_title}*
🗓️ {record_date}
⏰ {record_time}
📍 {record_place}
👤 PJ: {record_pj}
🆔 `{record_id}`

📝 *Agenda:*
{record_agenda}

🔗 Tersinkron ke *Portal LK-FEB* dan kalender `bem_feb_calendar.ics`."""
        self.client.send_message(chat_id, text)

    def cmd_reminder(self, chat_id: str, message: Dict[str, Any], args: str) -> None:
        args = bridge.clean_text(args)
        if not args or "|" not in args:
            self.client.send_message(
                chat_id,
                "⏰ *FORMAT REMINDER*\n\n"
                "`/reminder <waktu> | <isi>`\n\n"
                "Contoh:\n"
                "`/reminder Besok 09:00 | Kirim LPJ LKMM ke Dekanat`",
            )
            return

        waktu_raw, isi = [part.strip() for part in args.split("|", 1)]
        if not waktu_raw or not isi:
            self.client.send_message(
                chat_id, "⚠️ Waktu dan isi reminder tidak boleh kosong."
            )
            return

        schedule = bridge.parse_schedule(waktu_raw)
        payload = {
            "judul": f"Reminder: {bridge.truncate(isi, 80)}",
            "isi": isi,
            "tanggal": schedule["tanggal"],
            "waktu": schedule["waktu"],
            "waktu_teks": waktu_raw,
            "kategori": "Reminder",
            "pj": self._sender_name(message),
            "status": "Aktif",
            "source": "telegram",
        }
        try:
            record = bridge.add_reminder(payload, source="telegram")
        except Exception as exc:
            bridge.log(f"[TELEGRAM] Gagal menambah reminder: {exc}")
            self.client.send_message(
                chat_id, f"❌ *Gagal menyimpan reminder*\n\n`{exc}`"
            )
            return

        record_time = record["waktu"]
        record_date = bridge.format_tanggal_indonesia(record["tanggal"])
        record_body = record["isi"]
        record_id = record["id"]
        text = f"""✅ *REMINDER DISIMPAN*

⏰ *{record_time}*
🗓️ {record_date}
📝 {record_body}
🆔 `{record_id}`

🔔 Reminder juga masuk ke kalender BEM FEB."""
        self.client.send_message(chat_id, text)

    def cmd_akun(self, chat_id: str, message: Dict[str, Any]) -> None:
        accounts = bridge.load_accounts()
        active_id = accounts.get("active_profile")
        lines = ["🤖 *MULTI-ACCOUNT ANTIGRAVITY*", ""]
        for profile in bridge.accounts_as_list(accounts):
            marker = "✅" if profile.get("id") == active_id else "⚪"
            hand = " ♻️ _hand-me-down_" if profile.get("hand_me_down") else ""
            lines.append(
                f"{marker} `{profile.get('id')}` — {profile.get('name')}{hand}"
            )
            lines.append(f"    👤 {profile.get('owner', '—')}")
        lines.extend(
            [
                "",
                f"*Aktif sekarang:* `{active_id}`",
                "",
                "Ganti akun dengan:",
                "`/akun_switch <id>`",
                "",
                "Contoh:",
                "`/akun_switch sekretariat`",
            ]
        )
        self.client.send_message(chat_id, "\n".join(lines))

    def cmd_akun_switch(
        self, chat_id: str, message: Dict[str, Any], args: str
    ) -> None:
        profile_id = bridge.clean_text(args).split()[0] if bridge.clean_text(args) else ""
        if not profile_id:
            self.client.send_message(
                chat_id,
                "🔀 *GANTI AKUN ANTIGRAVITY*\n\n"
                "`/akun_switch <id>`\n\n"
                "Lihat daftar ID dengan `/akun`.",
            )
            return
        try:
            result = bridge.switch_profile(profile_id)
        except KeyError as exc:
            self.client.send_message(
                chat_id, f"❌ {str(exc).strip(chr(39))}"
            )
            return
        except Exception as exc:
            self.client.send_message(chat_id, f"❌ *Gagal mengganti akun*\n\n`{exc}`")
            return

        profile = result.get("profile") or {}
        active_id = result["active_profile"]
        profile_name = profile.get("name", "—")
        profile_owner = profile.get("owner", "—")
        profile_config = profile.get("config_path", "—")
        previous_id = result.get("previous_profile")
        text = f"""🔀 *AKUN ANTIGRAVITY DIPINDAHKAN*

✅ Aktif: `{active_id}`
📛 {profile_name}
👤 {profile_owner}
📁 `{profile_config}`

Sebelumnya: `{previous_id}`

_Perubahan langsung berlaku untuk bot dan eksekusi Antigravity berikutnya._"""
        self.client.send_message(chat_id, text)

    def cmd_notulensi(
        self, chat_id: str, message: Dict[str, Any], args: str
    ) -> None:
        query = bridge.clean_text(args)
        result = bridge.list_notulensi(include_content=False, query=query, limit=8)
        items = result["items"]
        if not items:
            self.client.send_message(
                chat_id,
                "📭 Belum ada notulensi"
                + (f" yang cocok dengan `{query}`." if query else "."),
            )
            return

        lines = ["📚 *ARSIP NOTULENSI BEM FEB*", ""]
        for index, item in enumerate(items, start=1):
            lines.append(
                f"{index}. *{bridge.truncate(item.get('judul', '—'), 90)}*"
            )
            lines.append(
                f"   🗓️ {bridge.format_tanggal_indonesia(item.get('tanggal', ''))}"
                f"  •  `{item.get('filename', '')}`"
            )
        lines.extend(
            [
                "",
                f"Total: *{result['total']}* notulensi",
                f"📁 `{bridge.NOTULENSI_DIR}`",
            ]
        )
        self.client.send_message(chat_id, "\n".join(lines))

    # ----- notulensi dari teks bebas ------------------------------------
    def _infer_metadata(
        self, text: str, message: Dict[str, Any]
    ) -> Dict[str, str]:
        fields = bridge.extract_labeled_fields(text)
        today = bridge.now_local().date()

        title = (
            fields.get("judul")
            or fields.get("agenda")
            or bridge.derive_title(text, f"Rapat BEM FEB {today.isoformat()}")
        )
        raw_date = fields.get("tanggal", "")
        raw_time = fields.get("waktu", "")
        schedule = bridge.parse_schedule(
            f"{raw_date} {raw_time}".strip(), default_date=today
        )
        # Bila tidak ada tanggal/waktu eksplisit, gunakan waktu sekarang.
        if not raw_date and not raw_time:
            current = bridge.now_local()
            schedule = bridge.parse_schedule(
                current.strftime("%Y-%m-%d %H:%M"), default_date=today
            )

        metadata: Dict[str, str] = {
            "judul": title,
            "agenda": fields.get("agenda") or title,
            "tanggal": schedule["tanggal"],
            "waktu": schedule["waktu"],
            "tempat": fields.get("tempat", ""),
            "pimpinan": fields.get("pimpinan")
            or self.config.get("owner_name")
            or "Arthur Reezan (Ketua BEM FEB)",
            "notulis": fields.get("notulis") or "Sekretaris Digital BEM FEB",
            "peserta": fields.get("peserta", ""),
            "sumber": "telegram",
        }
        related = self._find_related_meeting(metadata, text)
        if related:
            metadata["rapat_id"] = related.get("id", "")
            if related.get("tempat") and not metadata.get("tempat"):
                metadata["tempat"] = related["tempat"]
            if related.get("judul"):
                metadata["judul"] = related["judul"]
        return metadata

    def _find_related_meeting(
        self, metadata: Dict[str, str], text: str
    ) -> Optional[Dict[str, Any]]:
        data = bridge.load_meetings()
        meetings = data.get("meetings", [])
        title = bridge.clean_text(metadata.get("judul")).lower()
        text_lower = text.lower()
        candidates = sorted(
            meetings,
            key=lambda item: str(item.get("created_at", "")),
            reverse=True,
        )
        for meeting in candidates:
            meeting_title = bridge.clean_text(meeting.get("judul")).lower()
            if meeting_title and (
                meeting_title in text_lower or title in meeting_title
            ):
                return meeting
            if (
                bridge.clean_text(meeting.get("tanggal"))
                == bridge.clean_text(metadata.get("tanggal"))
                and meeting_title
                and title
                and _similar_title(meeting_title, title)
            ):
                return meeting
        return None

    def handle_note(
        self, chat_id: str, message: Dict[str, Any], text: str
    ) -> None:
        self.client.send_message(
            chat_id,
            "⏳ *Catatan diterima.*\n\n"
            "Saya sedang menyusunnya menjadi *Notulensi Resmi BEM FEB UKRIDA* "
            "dengan format Minutes of Meeting. Mohon tunggu sebentar…",
        )
        self.client.send_typing(chat_id)

        metadata = self._infer_metadata(text, message)
        metadata["sumber"] = "telegram"
        metadata["dikirim_oleh"] = self._sender_name(message)

        ai_used = False
        ai_error = ""
        content = ""
        if self.config.get("notulensi_ai_enabled", True):
            prompt = bridge.build_mom_prompt(text, metadata)
            try:
                result = bridge.run_antigravity(
                    prompt,
                    timeout=self.config["notulensi_ai_timeout"],
                    model=bridge.DEFAULT_MODEL,
                )
                if result.get("ok") and bridge.clean_text(result.get("stdout")):
                    candidate = bridge.strip_code_fences(result["stdout"])
                    if len(candidate) >= 80:
                        content = candidate
                        ai_used = True
                if not ai_used:
                    ai_error = bridge.clean_text(
                        result.get("error") or result.get("stderr")
                    )
            except Exception as exc:
                ai_error = str(exc)
                bridge.log(f"[TELEGRAM] Antigravity gagal: {exc}")

        if not content:
            content = bridge.build_mom_fallback(text, metadata)

        try:
            item = bridge.save_notulensi(
                content,
                metadata=metadata,
                source="telegram",
                raw_text=text,
            )
        except Exception as exc:
            bridge.log(f"[TELEGRAM] Gagal menyimpan notulensi: {exc}")
            self.client.send_message(
                chat_id,
                "❌ *Gagal menyimpan notulensi*\n\n"
                f"`{exc}`\n\nCatatan mentah Anda tetap aman di chat ini.",
            )
            return

        total = bridge.list_notulensi(limit=1)["total"]
        formatter = (
            "Antigravity DeepSeek (`antigravity/deepseek-v4.1-flash-free`)"
            if ai_used
            else "mode dasar (Antigravity belum tersedia)"
        )
        item_title = item.get("judul", "Notulensi Rapat")
        item_date = bridge.format_tanggal_indonesia(item.get("tanggal", ""))
        item_time = item.get("waktu") or "—"
        item_place = item.get("tempat") or "—"
        item_id = item.get("id", "—")
        item_path = item.get("relative_path", item.get("path", ""))
        text_reply = f"""✅ *NOTULENSI TERSIMPAN*

📄 *{item_title}*
🗓️ {item_date}
⏰ {item_time}
📍 {item_place}
🆔 `{item_id}`

🧠 *Format:* {formatter}
📁 `{item_path}`
📚 Total arsip: *{total}* notulensi

🔗 Notulensi otomatis tersedia di Portal LK-FEB."""
        if not ai_used:
            text_reply += (
                "\n\n⚠️ _Antigravity tidak merespons normal, sehingga notulensi "
                "disimpan dalam format dasar. Seluruh catatan mentah tetap dipertahankan._"
            )
            if ai_error:
                bridge.log(f"[TELEGRAM] Alasan fallback: {bridge.truncate(ai_error, 200)}")
        self.client.send_message(chat_id, text_reply)

    # ----- dispatcher ----------------------------------------------------
    def handle_update(self, update: Dict[str, Any]) -> None:
        if not isinstance(update, dict):
            return
        message = update.get("message")
        if not isinstance(message, dict):
            return
        if message.get("from", {}).get("is_bot"):
            return

        chat = message.get("chat") or {}
        chat_id = str(chat.get("id", ""))
        if not chat_id:
            return

        if not self._is_allowed(chat_id, message):
            bridge.log(
                f"[TELEGRAM] Akses ditolak untuk chat {chat_id} "
                f"({self._sender_name(message)})"
            )
            self.client.send_message(
                chat_id,
                "⛔ *Akses ditolak.*\n\n"
                f"Chat ID Anda: `{chat_id}`\n\n"
                "Minta Ketua BEM menambahkan ID ini ke `allowed_chat_ids` "
                "pada `config/telegram_config.json`.",
            )
            return

        text = bridge.clean_text(message.get("text") or message.get("caption"))
        if not text:
            self.client.send_message(
                chat_id,
                "ℹ️ Saat ini saya hanya dapat memproses pesan teks. "
                "Kirim catatan rapat dalam bentuk teks, atau gunakan `/help`.",
            )
            return

        if text.startswith("/"):
            match = re.match(
                r"^/([A-Za-z0-9_]+)(?:@[A-Za-z0-9_]+)?(?:\s+(.*))?$",
                text,
                flags=re.DOTALL,
            )
            if not match:
                self.cmd_help(chat_id, message)
                return
            command = match.group(1).lower()
            args = match.group(2) or ""

            if command in ("start", "help", "menu"):
                self.cmd_help(chat_id, message)
            elif command == "status":
                self.cmd_status(chat_id, message)
            elif command == "id":
                self.cmd_id(chat_id, message)
            elif command == "rapat":
                self.cmd_rapat(chat_id, message, args)
            elif command in ("reminder", "remind"):
                self.cmd_reminder(chat_id, message, args)
            elif command == "akun":
                self.cmd_akun(chat_id, message)
            elif command in ("akun_switch", "switch"):
                self.cmd_akun_switch(chat_id, message, args)
            elif command in ("notulensi", "notulen", "mom"):
                self.cmd_notulensi(chat_id, message, args)
            else:
                self.client.send_message(
                    chat_id,
                    f"❓ Perintah `/{command}` tidak dikenal.\n\n"
                    "Ketik `/help` untuk melihat menu.",
                )
            return

        # Teks bebas = catatan rapat → Minutes of Meeting.
        self.handle_note(chat_id, message, text)

    # ----- lifecycle -----------------------------------------------------
    def run(self) -> None:
        if not token_looks_configured(self.config["bot_token"]):
            reason = (
                "bot_token belum diisi atau masih placeholder di "
                f"{bridge.TELEGRAM_CONFIG_PATH}"
            )
            bridge.log(f"[TELEGRAM] {reason}")
            bridge.log(
                "[TELEGRAM] Bot tidak dijalankan. Isi bot_token & allowed_chat_ids, "
                "lalu restart start_bridge.py."
            )
            self._write_status("offline", reason)
            return

        bridge.log("[TELEGRAM] Menghubungi Bot API...")
        me: Dict[str, Any] = {}
        for attempt in range(1, 6):
            if self.stop_event.is_set():
                return
            try:
                me = self.client.get_me()
                break
            except TelegramError as exc:
                if exc.error_code in (401, 403):
                    self._write_status("error", f"Token ditolak Telegram: {exc}")
                    bridge.log(f"[TELEGRAM] Token ditolak: {exc}")
                    return
                bridge.log(
                    f"[TELEGRAM] Gagal getMe (percobaan {attempt}/5): {exc}"
                )
                self._write_status("offline", str(exc))
                self.stop_event.wait(min(30, attempt * 5))
        if not me:
            self._write_status("offline", "Tidak dapat terhubung ke Telegram")
            return

        username = bridge.clean_text(me.get("username"))
        with self.state_lock:
            self.status_state["username"] = username
            self.status_state["bot_id"] = me.get("id")
            self.status_state["bot_name"] = me.get("first_name")
        self._write_status("online", None)
        bridge.log(
            f"[TELEGRAM] Online sebagai @{username or me.get('first_name', 'bot')} "
            f"({len(self.config['allowed_chat_ids'])} chat diizinkan)"
        )

        commands = self.config.get("commands", {}).get("menu") or DEFAULT_COMMANDS
        try:
            self.client.set_my_commands(commands)
        except TelegramError as exc:
            bridge.log(f"[TELEGRAM] Gagal setMyCommands (diabaikan): {exc}")

        self.heartbeat_thread = threading.Thread(
            target=self._heartbeat_loop, name="telegram-heartbeat", daemon=True
        )
        self.heartbeat_thread.start()

        backoff = 3
        try:
            while not self.stop_event.is_set():
                try:
                    updates = self.client.get_updates(
                        offset=self.offset,
                        timeout=self.config["poll_timeout"],
                        allowed_updates=["message"],
                    )
                    backoff = 3
                    for update in updates:
                        if self.stop_event.is_set():
                            break
                        update_id = bridge.safe_int(update.get("update_id"), 0)
                        try:
                            self.handle_update(update)
                        except TelegramError as exc:
                            bridge.log(f"[TELEGRAM] Gagal membalas update: {exc}")
                        except Exception as exc:
                            bridge.log(f"[TELEGRAM] Error memproses update: {exc}")
                            try:
                                chat_id = (
                                    update.get("message", {}).get("chat", {}).get("id")
                                )
                                if chat_id:
                                    self.client.send_message(
                                        chat_id,
                                        "⚠️ Terjadi kesalahan internal saat memproses pesan. "
                                        "Silakan coba lagi.",
                                    )
                            except Exception:
                                pass
                        if update_id:
                            self.offset = max(self.offset, update_id + 1)
                            self._save_offset(self.offset)
                            with self.state_lock:
                                self.status_state["last_update_id"] = update_id
                    self._write_status("online", None)
                except TelegramError as exc:
                    if exc.error_code == 401:
                        self._write_status("error", f"Token ditolak: {exc}")
                        bridge.log("[TELEGRAM] Token ditolak, bot berhenti.")
                        break
                    if exc.error_code == 409:
                        self._write_status("error", f"Konflik polling: {exc}")
                        bridge.log(
                            "[TELEGRAM] Konflik 409: kemungkinan bot lain sedang "
                            "polling dengan token yang sama."
                        )
                        self.stop_event.wait(10)
                        continue
                    delay = exc.retry_after or backoff
                    self._write_status("offline", str(exc))
                    bridge.log(
                        f"[TELEGRAM] Error polling: {exc}. Retry dalam {delay}s."
                    )
                    self.stop_event.wait(delay)
                    backoff = min(backoff * 2, 60)
                except Exception as exc:
                    self._write_status("offline", str(exc))
                    bridge.log(
                        f"[TELEGRAM] Koneksi bermasalah: {exc}. Retry dalam {backoff}s."
                    )
                    self.stop_event.wait(backoff)
                    backoff = min(backoff * 2, 60)
        finally:
            self.stop_event.set()
            self._write_status("offline", "Bot dihentikan")
            bridge.log("[TELEGRAM] Bot berhenti.")


def _similar_title(left: str, right: str) -> bool:
    stopwords = {
        "rapat",
        "pleno",
        "bem",
        "feb",
        "ukrida",
        "dan",
        "the",
        "of",
        "yang",
        "untuk",
    }
    left_words = {
        word for word in re.findall(r"[a-z0-9]+", left.lower()) if word not in stopwords
    }
    right_words = {
        word for word in re.findall(r"[a-z0-9]+", right.lower()) if word not in stopwords
    }
    if not left_words or not right_words:
        return False
    overlap = len(left_words & right_words)
    return overlap >= 2 or overlap / max(1, min(len(left_words), len(right_words))) >= 0.6


def run_bot(stop_event: Optional[threading.Event] = None) -> None:
    bridge.ensure_runtime_files()
    bot = TelegramBot(stop_event=stop_event)
    bot.run()


def main() -> int:
    stop_event = threading.Event()

    def _handle_signal(signum: int, _frame: Any) -> None:
        bridge.log(f"[TELEGRAM] Sinyal {signum} diterima, menghentikan bot...")
        stop_event.set()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)
    run_bot(stop_event)
    return 0


if __name__ == "__main__":
    sys.exit(main())
