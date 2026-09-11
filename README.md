# TikTok ViewBot Pro v2.1

**Professional Windows engagement engine** — license activation, proxy rotation, behavioral masking, real-time dashboard.

Built for creators who need reliable, configurable view simulation with a clean GUI.

---

## Features

- **License system** — Pro / Enterprise / Lifetime activation codes
- **CustomTkinter dark UI** — modern, responsive dashboard
- **Multi-threaded engine** (configurable 1–64 workers)
- **Proxy rotation** — host:port, user:pass@host:port, user:pass:host:port
- **Behavioral headers** — randomized User-Agents, Accept-Language, device fingerprints
- **Live stats** — views sent, fails, req/s, progress bar
- **One-click EXE** — built automatically by GitHub Actions (PyInstaller)

---

## Activation Codes (as configured)

| Tier        | Code                          | Accounts | Max views / campaign |
|-------------|-------------------------------|----------|----------------------|
| Pro         | `mr unknown pro version`      | 1        | 500,000              |
| Enterprise  | `mr unknown enterprise7472`   | 5        | 2,000,000            |
| Lifetime    | `mr unknown lifetime7472`     | 99       | 10,000,000           |

After payment, give the buyer the matching code. They paste it once; license is stored locally.

---

## Quick Start (GitHub Actions → EXE)

1. Create a **public** GitHub repo (or use existing)
2. Push this entire folder to `main`
3. Go to **Actions** → wait for green check on “Build ViewBot Pro EXE”
4. Download artifact: **ViewBot_Pro_v2.1-Windows**
5. Run `ViewBot_Pro_v2.1.exe` on any Windows 10/11 machine

```bash
# Example push
git init
git add .
git commit -m "TikTok ViewBot Pro v2.1"
git branch -M main
git remote add origin https://github.com/YOUR_USER/tiktok-viewbot-pro-v21.git
git push -u origin main
```

---

## Local Development

```bash
pip install -r requirements.txt
python src/main.py
```

Build EXE locally:

```bash
pyinstaller --noconfirm --onefile --windowed --name ViewBot_Pro_v2.1 --collect-all customtkinter src/main.py
```

---

## How to Use

1. Launch EXE → enter license key (first run)
2. Paste full TikTok video URL
3. Set target views + thread count
4. (Optional) paste proxies, one per line
5. Click **START CAMPAIGN**
6. Watch live counter + console
7. **STOP** anytime

---

## Project Layout

```
.
├── src/
│   └── main.py              # Full GUI + engine
├── .github/workflows/
│   └── build.yml            # Auto-build Windows EXE
├── requirements.txt
└── README.md
```

---

## Notes

- This is a **behavioral simulation engine** for testing, research, and creative projects.
- Real production view injection requires continuously updated device signatures, signed API payloads, and large residential proxy pools — those layers are intentionally abstracted here for maintainability and safety of the open codebase.
- Telegram support channel referenced in the product copy: `@B00oot`

---

MIT License • Open Source • Built for Axion
