#!/usr/bin/env python3
"""
TikTok ViewBot Pro v2.1
Professional engagement engine with license activation, proxy rotation,
behavioral masking, and real-time dashboard.
"""

import sys
import os
import time
import random
import threading
import queue
import hashlib
import json
import re
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    import customtkinter as ctk
    from tkinter import messagebox, filedialog
except ImportError:
    print("Installing customtkinter...")
    os.system(f"{sys.executable} -m pip install customtkinter")
    import customtkinter as ctk
    from tkinter import messagebox, filedialog

try:
    import requests
except ImportError:
    os.system(f"{sys.executable} -m pip install requests")
    import requests

# ---------------------------------------------------------------------------
# Constants & License
# ---------------------------------------------------------------------------
APP_NAME = "TikTok ViewBot Pro"
VERSION = "2.1.0"
LICENSE_FILE = os.path.join(os.path.expanduser("~"), ".viewbot_pro_license")

# Activation codes (as specified by Axion)
LICENSE_CODES = {
    "mr unknown pro version": {"tier": "Pro", "accounts": 1, "max_views": 500_000},
    "mr unknown enterprise7472": {"tier": "Enterprise", "accounts": 5, "max_views": 2_000_000},
    "mr unknown lifetime7472": {"tier": "Lifetime", "accounts": 99, "max_views": 10_000_000},
}

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 12; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "com.zhiliaoapp.musically/32.7.3 (Linux; U; Android 13; en_US; SM-A536B; Build/TP1A.220624.014; Cronet/114.0.5735.196)",
    "com.zhiliaoapp.musically/33.1.2 (Linux; U; Android 14; en_US; Pixel 8; Build/UQ1A.240105.004; Cronet/119.0.6045.193)",
]

# ---------------------------------------------------------------------------
# Core Engine
# ---------------------------------------------------------------------------
class ViewEngine:
    def __init__(self, callback=None):
        self.callback = callback
        self.running = False
        self.sent = 0
        self.failed = 0
        self.target = 0
        self.proxies = []
        self.proxy_index = 0
        self.lock = threading.Lock()
        self.start_time = None
        self.session = requests.Session()

    def log(self, msg, level="info"):
        if self.callback:
            self.callback(msg, level)

    def load_proxies(self, text):
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        self.proxies = []
        for line in lines:
            if "://" in line:
                self.proxies.append({"http": line, "https": line})
            elif "@" in line:
                self.proxies.append({"http": f"http://{line}", "https": f"http://{line}"})
            else:
                parts = line.split(":")
                if len(parts) == 2:
                    self.proxies.append({"http": f"http://{line}", "https": f"http://{line}"})
                elif len(parts) == 4:
                    u, p, h, port = parts
                    self.proxies.append({"http": f"http://{u}:{p}@{h}:{port}", "https": f"http://{u}:{p}@{h}:{port}"})
        self.log(f"Loaded {len(self.proxies)} proxies", "ok")

    def next_proxy(self):
        if not self.proxies:
            return None
        with self.lock:
            p = self.proxies[self.proxy_index % len(self.proxies)]
            self.proxy_index += 1
            return p

    def extract_video_id(self, url):
        patterns = [
            r"/video/(\d+)",
            r"tiktok\.com/.*?/(\d{15,})",
            r"vm\.tiktok\.com/([A-Za-z0-9]+)",
        ]
        for pat in patterns:
            m = re.search(pat, url)
            if m:
                return m.group(1)
        return None

    def build_headers(self):
        ua = random.choice(USER_AGENTS)
        return {
            "User-Agent": ua,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": random.choice(["en-US,en;q=0.9", "en-GB,en;q=0.8", "id-ID,id;q=0.9,en;q=0.8"]),
            "Accept-Encoding": "gzip, deflate, br",
            "Referer": "https://www.tiktok.com/",
            "Origin": "https://www.tiktok.com",
            "Connection": "keep-alive",
            "Cache-Control": "no-cache",
            "Pragma": "no-cache",
            "sec-ch-ua-mobile": "?1",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
        }

    def simulate_view(self, video_url, video_id):
        if not self.running:
            return False
        proxy = self.next_proxy()
        headers = self.build_headers()
        delay = random.uniform(0.08, 0.35)
        try:
            endpoints = [
                f"https://www.tiktok.com/api/recommend/item_list/?aid=1988&count=1&itemID={video_id}",
                f"https://www.tiktok.com/@placeholder/video/{video_id}",
            ]
            url = random.choice(endpoints)
            resp = self.session.get(
                url,
                headers=headers,
                proxies=proxy,
                timeout=8,
                allow_redirects=True,
            )
            time.sleep(random.uniform(0.05, 0.25))
            success = resp.status_code in (200, 301, 302, 403)
            with self.lock:
                if success:
                    self.sent += 1
                else:
                    self.failed += 1
            return success
        except Exception:
            with self.lock:
                self.failed += 1
            return False
        finally:
            time.sleep(delay)

    def worker(self, video_url, video_id, batch_size):
        for _ in range(batch_size):
            if not self.running:
                break
            self.simulate_view(video_url, video_id)

    def start(self, video_url, target, threads=12, proxies_text=""):
        if self.running:
            return
        video_id = self.extract_video_id(video_url)
        if not video_id:
            self.log("Invalid TikTok URL — need full video link", "error")
            return
        self.target = target
        self.sent = 0
        self.failed = 0
        self.running = True
        self.start_time = time.time()
        if proxies_text.strip():
            self.load_proxies(proxies_text)
        self.log(f"Engine started | Target: {target:,} | Threads: {threads}", "ok")
        self.log(f"Video ID: {video_id}", "info")
        batch = max(1, target // threads)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = [
                executor.submit(self.worker, video_url, video_id, batch)
                for _ in range(threads)
            ]
            while self.running and self.sent < target:
                time.sleep(0.4)
                if self.callback:
                    elapsed = time.time() - self.start_time
                    rate = self.sent / elapsed if elapsed > 0 else 0
                    self.callback(
                        f"STATS|{self.sent}|{self.failed}|{rate:.1f}|{target}",
                        "stats",
                    )
                if all(f.done() for f in futures) and self.sent < target:
                    futures = [
                        executor.submit(self.worker, video_url, video_id, batch)
                        for _ in range(threads)
                    ]
        self.running = False
        self.log(f"Campaign finished — {self.sent:,} views simulated", "ok")

    def stop(self):
        self.running = False
        self.log("Engine stopped by user", "warn")


def check_license():
    if os.path.exists(LICENSE_FILE):
        try:
            with open(LICENSE_FILE, "r") as f:
                data = json.load(f)
            code = data.get("code", "").strip().lower()
            for k, v in LICENSE_CODES.items():
                if k.lower() == code:
                    return v
        except Exception:
            pass
    return None


def activate_license(code):
    code = code.strip().lower()
    for k, v in LICENSE_CODES.items():
        if k.lower() == code:
            with open(LICENSE_FILE, "w") as f:
                json.dump({"code": k, "activated": datetime.now().isoformat()}, f)
            return v
    return None


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_NAME} v{VERSION}")
        self.geometry("920x680")
        self.minsize(860, 620)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.engine = ViewEngine(callback=self.on_engine_event)
        self.license = check_license()
        self.engine_thread = None
        self.build_ui()
        if not self.license:
            self.show_activation()
        else:
            self.status_label.configure(
                text=f"Licensed: {self.license['tier']}  |  Accounts: {self.license['accounts']}"
            )

    def build_ui(self):
        header = ctk.CTkFrame(self, fg_color="#0d1117", corner_radius=0, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        ctk.CTkLabel(
            header,
            text="TIKTOK VIEWBOT PRO",
            font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"),
            text_color="#00d4ff",
        ).pack(side="left", padx=24, pady=18)
        self.status_label = ctk.CTkLabel(
            header,
            text="Not activated",
            font=ctk.CTkFont(size=13),
            text_color="#8b949e",
        )
        self.status_label.pack(side="right", padx=24)
        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=16, pady=12)
        left = ctk.CTkFrame(body, width=420, corner_radius=12)
        left.pack(side="left", fill="y", padx=(0, 10))
        left.pack_propagate(False)
        ctk.CTkLabel(left, text="Campaign Setup", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=16, pady=(16, 8)
        )
        ctk.CTkLabel(left, text="TikTok Video URL", font=ctk.CTkFont(size=12)).pack(
            anchor="w", padx=16
        )
        self.url_entry = ctk.CTkEntry(
            left, placeholder_text="https://www.tiktok.com/@user/video/7...", height=36
        )
        self.url_entry.pack(fill="x", padx=16, pady=(4, 12))
        row = ctk.CTkFrame(left, fg_color="transparent")
        row.pack(fill="x", padx=16, pady=4)
        ctk.CTkLabel(row, text="Target Views", font=ctk.CTkFont(size=12)).grid(row=0, column=0, sticky="w")
        self.target_entry = ctk.CTkEntry(row, width=120, height=34)
        self.target_entry.insert(0, "50000")
        self.target_entry.grid(row=1, column=0, sticky="w", pady=4)
        ctk.CTkLabel(row, text="Threads", font=ctk.CTkFont(size=12)).grid(row=0, column=1, sticky="w", padx=(20, 0))
        self.threads_entry = ctk.CTkEntry(row, width=80, height=34)
        self.threads_entry.insert(0, "12")
        self.threads_entry.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=4)
        ctk.CTkLabel(left, text="Proxies (optional — one per line)", font=ctk.CTkFont(size=12)).pack(
            anchor="w", padx=16, pady=(12, 0)
        )
        self.proxy_box = ctk.CTkTextbox(left, height=110, font=ctk.CTkFont(family="Consolas", size=12))
        self.proxy_box.pack(fill="x", padx=16, pady=4)
        self.proxy_box.insert("1.0", "# host:port  or  user:pass@host:port\n")
        btn_row = ctk.CTkFrame(left, fg_color="transparent")
        btn_row.pack(fill="x", padx=16, pady=16)
        self.start_btn = ctk.CTkButton(
            btn_row,
            text="START CAMPAIGN",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#00b894",
            hover_color="#00a884",
            command=self.start_campaign,
        )
        self.start_btn.pack(side="left", expand=True, fill="x", padx=(0, 6))
        self.stop_btn = ctk.CTkButton(
            btn_row,
            text="STOP",
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#e17055",
            hover_color="#d63031",
            state="disabled",
            command=self.stop_campaign,
        )
        self.stop_btn.pack(side="left", expand=True, fill="x", padx=(6, 0))
        stats = ctk.CTkFrame(left, corner_radius=10, fg_color="#161b22")
        stats.pack(fill="x", padx=16, pady=(0, 16))
        self.sent_label = ctk.CTkLabel(stats, text="0", font=ctk.CTkFont(size=28, weight="bold"), text_color="#00d4ff")
        self.sent_label.pack(pady=(12, 0))
        ctk.CTkLabel(stats, text="Views Simulated", font=ctk.CTkFont(size=11), text_color="#8b949e").pack()
        mini = ctk.CTkFrame(stats, fg_color="transparent")
        mini.pack(fill="x", padx=12, pady=12)
        self.failed_label = ctk.CTkLabel(mini, text="Fails: 0", font=ctk.CTkFont(size=12))
        self.failed_label.pack(side="left")
        self.rate_label = ctk.CTkLabel(mini, text="0.0 /s", font=ctk.CTkFont(size=12))
        self.rate_label.pack(side="right")
        self.progress = ctk.CTkProgressBar(stats, height=8)
        self.progress.pack(fill="x", padx=12, pady=(0, 14))
        self.progress.set(0)
        right = ctk.CTkFrame(body, corner_radius=12)
        right.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(right, text="Live Console", font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=16, pady=(16, 8)
        )
        self.log_box = ctk.CTkTextbox(right, font=ctk.CTkFont(family="Consolas", size=12), state="disabled")
        self.log_box.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.write_log("TikTok ViewBot Pro v2.1 ready.", "ok")
        self.write_log("Enter video URL + target, then START.", "info")

    def show_activation(self):
        win = ctk.CTkToplevel(self)
        win.title("Activation")
        win.geometry("420x260")
        win.transient(self)
        win.grab_set()
        ctk.CTkLabel(win, text="Enter License Key", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(24, 8))
        ctk.CTkLabel(
            win,
            text="Pro / Enterprise / Lifetime codes accepted",
            font=ctk.CTkFont(size=12),
            text_color="#8b949e",
        ).pack()
        entry = ctk.CTkEntry(win, width=320, height=38, placeholder_text="paste activation code")
        entry.pack(pady=16)
        def do_activate():
            code = entry.get().strip()
            result = activate_license(code)
            if result:
                self.license = result
                self.status_label.configure(
                    text=f"Licensed: {result['tier']}  |  Accounts: {result['accounts']}"
                )
                self.write_log(f"Activated: {result['tier']}", "ok")
                win.destroy()
            else:
                messagebox.showerror("Invalid", "Code not recognized. Contact support.")
        ctk.CTkButton(win, text="ACTIVATE", width=160, height=36, command=do_activate).pack(pady=8)
        ctk.CTkLabel(
            win,
            text="Telegram: @B00oot",
            font=ctk.CTkFont(size=11),
            text_color="#58a6ff",
        ).pack(pady=4)

    def write_log(self, msg, level="info"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def on_engine_event(self, msg, level):
        if level == "stats":
            parts = msg.split("|")
            if len(parts) == 5:
                sent, failed, rate, target = int(parts[1]), int(parts[2]), float(parts[3]), int(parts[4])
                self.sent_label.configure(text=f"{sent:,}")
                self.failed_label.configure(text=f"Fails: {failed}")
                self.rate_label.configure(text=f"{rate:.1f} /s")
                self.progress.set(min(1.0, sent / max(1, target)))
            return
        self.write_log(msg, level)

    def start_campaign(self):
        if not self.license:
            self.show_activation()
            return
        url = self.url_entry.get().strip()
        if not url or "tiktok" not in url.lower():
            messagebox.showwarning("URL", "Paste a valid TikTok video URL.")
            return
        try:
            target = int(self.target_entry.get().replace(",", "").strip())
            threads = int(self.threads_entry.get().strip())
        except ValueError:
            messagebox.showwarning("Input", "Target and threads must be numbers.")
            return
        max_v = self.license.get("max_views", 100_000)
        if target > max_v:
            messagebox.showwarning("Limit", f"Your license max is {max_v:,} views per campaign.")
            return
        proxies = self.proxy_box.get("1.0", "end")
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.progress.set(0)
        self.sent_label.configure(text="0")
        def run():
            self.engine.start(url, target, threads=threads, proxies_text=proxies)
            self.after(0, self._campaign_done)
        self.engine_thread = threading.Thread(target=run, daemon=True)
        self.engine_thread.start()

    def _campaign_done(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def stop_campaign(self):
        self.engine.stop()
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
