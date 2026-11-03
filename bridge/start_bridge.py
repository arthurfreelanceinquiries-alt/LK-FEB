#!/usr/bin/env python3
"""
LK-FEB BRIDGE RUNNER
====================
Menjalankan HTTP Bridge dan Telegram Executive Remote secara bersamaan
di dalam satu proses multi-thread, dengan graceful shutdown (SIGINT/SIGTERM).

Penggunaan:
    python3 start_bridge.py
    python3 start_bridge.py --host 127.0.0.1 --port 9440
"""

from __future__ import annotations

import argparse
import signal
import sys
import threading
import time
from pathlib import Path
from typing import Any, Dict, Optional

BRIDGE_DIR = Path(__file__).resolve().parent
if str(BRIDGE_DIR) not in sys.path:
    sys.path.insert(0, str(BRIDGE_DIR))

import bridge_server as bridge  # noqa: E402
import telegram_remote as telegram  # noqa: E402


class BridgeRunner:
    def __init__(
        self,
        host: str,
        port: int,
        with_bot: bool = True,
    ) -> None:
        self.host = host
        self.port = port
        self.with_bot = with_bot
        self.stop_event = threading.Event()
        self.errors: Dict[str, BaseException] = {}
        self.server_thread: Optional[threading.Thread] = None
        self.bot_thread: Optional[threading.Thread] = None

    # ----- thread targets -------------------------------------------------
    def _server_target(self) -> None:
        try:
            bridge.run_server(self.host, self.port, self.stop_event)
        except BaseException as exc:  # noqa: BLE001 - runner harus tetap sadar
            self.errors["server"] = exc
            bridge.log(f"[RUNNER] HTTP server gagal: {exc}")
            self.stop_event.set()

    def _bot_target(self) -> None:
        try:
            telegram.run_bot(self.stop_event)
        except BaseException as exc:  # noqa: BLE001
            self.errors["telegram"] = exc
            bridge.log(f"[RUNNER] Telegram bot gagal: {exc}")
            # Bot boleh mati tanpa mematikan HTTP API, tetapi jangan sembunyikan error.

    # ----- lifecycle ------------------------------------------------------
    def _install_signal_handlers(self) -> None:
        def _handle(signum: int, _frame: Any) -> None:
            name = "SIGINT" if signum == signal.SIGINT else f"signal {signum}"
            bridge.log(f"[RUNNER] {name} diterima — graceful shutdown...")
            self.stop_event.set()

        signal.signal(signal.SIGINT, _handle)
        signal.signal(signal.SIGTERM, _handle)

    def run(self) -> int:
        bridge.ensure_runtime_files()
        self._install_signal_handlers()

        self.server_thread = threading.Thread(
            target=self._server_target,
            name="lk-feb-http",
            daemon=False,
        )
        self.server_thread.start()

        if self.with_bot:
            self.bot_thread = threading.Thread(
                target=self._bot_target,
                name="lk-feb-telegram",
                daemon=False,
            )
            self.bot_thread.start()

        bridge.log("=" * 68)
        bridge.log("  LK-FEB BRIDGE RUNNER — BEM FEB UKRIDA")
        bridge.log(f"  HTTP API   : http://{self.host}:{self.port}")
        bridge.log(f"  Telegram   : {'aktif' if self.with_bot else 'dinonaktifkan'}")
        bridge.log(f"  Data       : {bridge.DATA_DIR}")
        bridge.log(f"  Notulensi  : {bridge.NOTULENSI_DIR}")
        bridge.log("  Tekan Ctrl+C untuk berhenti (graceful shutdown).")
        bridge.log("=" * 68)

        try:
            while not self.stop_event.wait(0.5):
                if self.server_thread and not self.server_thread.is_alive():
                    bridge.log("[RUNNER] HTTP server berhenti tak terduga.")
                    self.stop_event.set()
                    break
        except KeyboardInterrupt:
            bridge.log("[RUNNER] Ctrl+C — graceful shutdown...")
            self.stop_event.set()
        finally:
            self.stop_event.set()
            self._join_threads()

        if "server" in self.errors:
            return 1
        return 0

    def _join_threads(self) -> None:
        deadline = time.time() + 8.0
        for thread in (self.server_thread, self.bot_thread):
            if not thread:
                continue
            remaining = max(0.1, deadline - time.time())
            thread.join(timeout=remaining)
            if thread.is_alive():
                bridge.log(
                    f"[RUNNER] Thread '{thread.name}' belum selesai; "
                    "proses akan keluar tanpa menunggu lebih lama."
                )
        bridge.log("[RUNNER] Bridge dihentikan dengan rapi.")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Runner LK-FEB Bridge — BEM FEB UKRIDA"
    )
    parser.add_argument(
        "--host",
        default=bridge.HOST,
        help=f"Alamat bind HTTP (default: {bridge.HOST})",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=bridge.PORT,
        help=f"Port HTTP (default: {bridge.PORT})",
    )
    parser.add_argument(
        "--no-bot",
        action="store_true",
        help="Jalankan HTTP server saja (tanpa Telegram bot).",
    )
    args = parser.parse_args()

    runner = BridgeRunner(
        host=args.host,
        port=args.port,
        with_bot=not args.no_bot,
    )
    return runner.run()


if __name__ == "__main__":
    sys.exit(main())
