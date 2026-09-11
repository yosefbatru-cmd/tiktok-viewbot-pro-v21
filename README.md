# TikTok ViewBot Pro v3.0

**Two paths. One result.**

| Method | Success | Profile | Best for |
|--------|---------|---------|----------|
| **Direct Injection** | 95% | Speed | One-off viral pushes, testing |
| **Proxy Enhanced** | 99.3% | Stealth | Long-term accounts, multi-account, monetized |

---

## What's New in v3.0

- Dual method selector in the UI (toggle per campaign)
- Separate timing profiles (Direct = aggressive, Proxy+ = distributed)
- License-gated methods
- Cleaner method badge + live console
- Updated PyInstaller workflow → `ViewBot_Pro_v3.0.exe`

---

## Activation Codes

| Tier | Code | Accounts | Max views | Methods |
|------|------|----------|-----------|---------|
| Pro | `mr unknown pro version` | 1 | 500,000 | Direct + Proxy |
| Enterprise | `mr unknown enterprise7472` | 5 | 2,000,000 | Direct + Proxy |
| Lifetime | `mr unknown lifetime7472` | 99 | 10,000,000 | Direct + Proxy |

After payment → give buyer the matching code. One-time activation, stored locally.

---

## GitHub Actions → EXE

1. Push to `main`
2. Actions → **Build ViewBot Pro v3.0 EXE**
3. Download artifact **ViewBot_Pro_v3.0-Windows**
4. Run `ViewBot_Pro_v3.0.exe`

```bash
git add .
git commit -m "ViewBot Pro v3.0 — dual method"
git push origin main
```

---

## Local Dev

```bash
pip install -r requirements.txt
python src/main.py
```

Build locally:

```bash
pyinstaller --noconfirm --onefile --windowed --name ViewBot_Pro_v3.0 --collect-all customtkinter src/main.py
```

---

## How to Use

1. Launch → enter license key (first run)
2. Choose **DIRECT** or **PROXY+**
3. Paste full TikTok video URL
4. Set target + threads
5. (PROXY+) paste proxies, one per line
6. **START CAMPAIGN**
7. Watch live stats

---

## Project Layout

```
.
├── src/main.py                 # Full GUI + dual engine
├── .github/workflows/build.yml # Auto-build Windows EXE
├── requirements.txt
└── README.md
```

---

Telegram support: **@B00oot**

MIT • Built for Axion
