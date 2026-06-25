import os, sys, json, subprocess, urllib.request, threading

VERSION_URL = "https://raw.githubusercontent.com/Lux00001/8Ball/main/version.json"
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PENDING_FILE = os.path.join(BASE, "_update_pending.json")

def _local_ver():
    p = os.path.join(BASE, "version.json")
    try:
        with open(p) as f:
            return json.load(f).get("version", "0.0.0")
    except Exception:
        return "0.0.0"

def _check_pending(term_write):
    if not os.path.exists(PENDING_FILE):
        return
    try:
        with open(PENDING_FILE) as f:
            target = json.load(f).get("target", "")
        os.remove(PENDING_FILE)
        current = _local_ver()
        if current == target:
            term_write(f"[8Ball] Update to v{target} successful.\n")
        else:
            term_write(f"[8Ball] Update failed: expected v{target}, got v{current}.\n")
    except Exception:
        try:
            os.remove(PENDING_FILE)
        except Exception:
            pass

def _check(term_write, ask_user, on_restart):
    term_write("[8Ball] Checking for update...\n")
    try:
        req = urllib.request.Request(VERSION_URL, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        remote = data.get("version", "")
        if not remote or remote == _local_ver():
            term_write("[8Ball] Up to date.\n")
            return
        term_write(f"[8Ball] Updating to v{remote}...\n")
        if not ask_user(f"Version {remote} is available.\nDownload and update now?"):
            term_write("[8Ball] Update skipped.\n")
            return
        with open(PENDING_FILE, "w") as f:
            json.dump({"target": remote}, f)
        _apply(data, remote, term_write)
        on_restart()
    except Exception:
        term_write("[8Ball] Update check failed (offline or no remote).\n")

def _apply(data, remote, term_write):
    raw = data.get("files", [])
    if isinstance(raw, dict):
        items = [{"url": u, "path": k} for k, u in raw.items()]
    elif isinstance(raw, list):
        items = raw
    else:
        items = []
    pending = []
    self_path = os.path.abspath(__file__)
    for entry in items:
        if not isinstance(entry, dict):
            continue
        url = entry.get("url")
        rel_path = entry.get("path")
        if not url or not rel_path:
            continue
        full_path = os.path.join(BASE, rel_path)
        full_path = os.path.abspath(full_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            content = resp.read()
        except Exception as e:
            term_write(f"[8Ball] Download failed for {rel_path}: {e}\n")
            return
        if full_path == os.path.join(BASE, "builder.pyw") or full_path == self_path:
            tmp = full_path + ".update.tmp"
            with open(tmp, "wb") as f:
                f.write(content)
            pending.append((full_path, tmp))
        else:
            with open(full_path, "wb") as f:
                f.write(content)
    # Write version.json to a temp file too — batch will move it after swapping
    ver_path = os.path.join(BASE, "version.json")
    ver_tmp = ver_path + ".update.tmp"
    with open(ver_tmp, "w") as f:
        json.dump({"version": remote, "files": raw}, f, indent=2)
    pending.append((ver_path, ver_tmp))
    if pending:
        pid = os.getpid()
        bat_path = os.path.join(BASE, "_update.bat")
        moves = "\n".join(f'move /Y "{src}" "{dst}" >nul' for dst, src in pending)
        with open(bat_path, "w") as f:
            f.write(f"""@echo off
taskkill /F /PID {pid} >nul 2>&1
{moves}
start "" "{os.path.join(BASE, "builder.pyw")}"
del "%~f0"
""")
        try:
            subprocess.Popen(f'cmd /c "{bat_path}"', creationflags=subprocess.CREATE_NO_WINDOW)
            term_write("[8Ball] Update complete. Restarting...\n")
        except Exception as e:
            term_write(f"[8Ball] Failed to launch updater: {e}\n")
    else:
        term_write("[8Ball] Update complete.\n")

def start(term_write, ask_user, on_restart):
    _check_pending(term_write)
    threading.Thread(target=_check, args=(term_write, ask_user, on_restart), daemon=True).start()
