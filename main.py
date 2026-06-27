import os
import sys
import subprocess
import time
import random
import string
import threading
from concurrent.futures import ThreadPoolExecutor

def install_missing_packages():
    for package in ['requests', 'colorama']:
        try:
            __import__(package)
        except ImportError:
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", package])
            except: pass

install_missing_packages()

import requests
from colorama import Fore, init

init(autoreset=True)

TOKENS = [ 
"token there" 
]

API_URL = 'https://discord.com/api/v9/users/@me/pomelo-attempt'

webhook_url = ""
mode_choice = ""
user_len = 4
delay = 0.02
token_index = 0
proxy_index = 0
PROXIES_LIST = []

# أقفال الحماية (Locks)
token_lock = threading.Lock()
proxy_lock = threading.Lock()
checked_set = set()
set_lock = threading.Lock()
file_lock = threading.Lock()

def cls():
    os.system('clear' if os.name != 'nt' else 'cls')

def load_proxies():
    global PROXIES_LIST
    if os.path.exists('proxies.txt'):
        with open('proxies.txt', 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            for line in lines:
                line = line.strip()
                if line:
                    # تحويل صيغة البروكسي لتناسب مكتبة requests
                    if "@" in line:
                        proxy_dict = {"http": f"http://{line}", "https": f"http://{line}"}
                    else:
                        proxy_dict = {"http": f"http://{line}", "https": f"http://{line}"}
                    PROXIES_LIST.append(proxy_dict)
        print(Fore.GREEN + f"[+] Loaded {len(PROXIES_LIST)} proxies from proxies.txt")
    else:
        # إنشاء ملف فارغ إذا لم يكن موجوداً لتنبيه المستخدم
        with open('proxies.txt', 'w') as f:
            pass
        print(Fore.YELLOW + "[!] proxies.txt not found. Created an empty one. Running without proxies.")

def get_next_token():
    global token_index
    with token_lock:
        if not TOKENS:
            return None
        token = TOKENS[token_index % len(TOKENS)]
        token_index += 1
        return token

def get_next_proxy():
    global proxy_index
    with proxy_lock:
        if not PROXIES_LIST:
            return None
        proxy = PROXIES_LIST[proxy_index % len(PROXIES_LIST)]
        proxy_index += 1
        return proxy

def generate_random_user(length=4):
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    while True:
        user = ''.join(random.choice(chars + ".") for _ in range(length))
        if user.startswith('.') or user.endswith('.') or ".." in user:
            continue
        return user

def generate_semi_user(length=4):
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    if length < 3: length = 3
    base = ''.join(random.choice(chars) for _ in range(length - 1))
    user_list = list(base)
    if random.choice(["dot", "under"]) == "dot":
        pos = random.choice(range(1, len(user_list)))
        user_list.insert(pos, ".")
    else:
        pos = random.choice([1, len(user_list)])
        user_list.insert(pos, "_")
    return "".join(user_list)

def generate_double_user(length=4):
    chars = "abcdefghijklmnopqrstuvwxyz1234567890"
    if length < 3: length = 3
    double_char = random.choice(chars)
    remaining_len = length - 2
    remaining_chars = ''.join(random.choice(chars) for _ in range(remaining_len))
    
    user_list = list(remaining_chars)
    insert_pos = random.randint(0, len(user_list))
    user_list.insert(insert_pos, double_char * 2)
    return "".join(user_list)

def send_webhook_worker(username, url):
    data = {
        "embeds": [{
            "title": "🎯 New Username Available!",
            "description": f"**User:** `{username}`\n**Status:** `AVAILABLE`",
            "color": 5763719
        }]
    }
    try:
        requests.post(url, json=data, timeout=5)
    except:
        pass

def send_webhook_async(username):
    if not webhook_url: return
    threading.Thread(target=send_webhook_worker, args=(username, webhook_url), daemon=True).start()

BANNER = rf"""
{Fore.CYAN}
,%@&(                                        
                                @@@@@@@@@@@@@%                                  
                                .@@@@@@@@@@@@@@@@@(                                
                                @@@@@@@@@@@@@@@@@@@#                               
                                (@@@@@&  @@@@  @@@@@@.                              
                                @@@@&   @@@* @@@@@(        @@@@@@@@              
                    ,  /         ,@@@. *@@@@@* @@@@&        @@@@@ @@/ @&            
                @@@@@@@@@       /@@@@@@@@@@@@@@@@@@@@        &@&  @* @@  #%           
            @@ @@.&@@(@@@@    (@@@@@@#    ,.@@@@@@@@@    &@@(  %   @                
            @ ,@/ @* &@@@@@@@@@@@, @@@@% ((@@@@@@@@@@@@      /&                  
                #(  &@#  &@@@@@@@@@@@&@@@@@@@@# @@@@@@@@@@,                         
                        &@@@@@@@@@@@@@@@@@@@@@@ @@@@@@@@@@                        
                        &@@@@@@@@@@@@@@@@@@@@@#&@@@@@@@@@@@                       
                        &. /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                      
                        @  /@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,/                      
                        , #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ //                      
                        ,  (,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                            @*@@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                            @ @@@@@@@@@@@@@@@@@@@@@@@@@@@@                        
                            @ @ @@@@@@@@@@@@@@@@@@@@@@@@@%                        
                            ,(#   * *@#@@@@@@@@@@@@@@@@@@ & @                      
                                     @%@@@@@@@@@@@@@@@@@/ ..                         
                                     @@@@@@@@@@@@@@@@@@#                                
                                     *.@@@@@@@@@@@@@@@&,                                
                                     #%@@/ @@@@@@@@ @                                  
                                     %.*@  *@@@@@@@ (                                  
                                     (  @   @@@@@@                                    
                                         @   &@@@@@                                    
                                         @   @@@.@                                     
                                             #@* /@* &@
.d8888b.  db       db      .d8b.  d888888b d8b   db d88888b d8888b. db   dD 
d8'   `8b 88       88     d8' `8b   `88'   888o  88 88'     88  `8D 88 ,8P' 
`8b.      88       88     88ooo88    88    88V8o 88 88ooooo 88oobY' 88,8P   
  `Y8b.    88       88     88~~~88    88    88 V8o88 88~~~~~ 88`8b   88`8b   
db   8D  88booo.  88booo. 88   88   .88.   88  V888 88.     88 `88. 88 `88. 
`8888Y'   Y88888P  Y88888P YP   YP Y888888P VP   V8P Y88888P 88   YD YP   YD
            [ SYSTEM: FIXED-STATION v12.0 - Sulaiman-DEV ]
"""

def check_worker():
    while True:
        while True:
            if mode_choice == "2":
                target_user = generate_semi_user(user_len)
            elif mode_choice == "3":
                target_user = generate_double_user(user_len)
            else:
                target_user = generate_random_user(user_len)
            
            with set_lock:
                if target_user not in checked_set:
                    checked_set.add(target_user)
                    break

        token = get_next_token()
        proxy = get_next_proxy()
        
        headers = {
            'Authorization': token if token else "",
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            # تم إضافة البروكسي هنا بشكل مرن (إذا لم يتوفر بروكسي سيعمل بدونه)
            r = requests.post(API_URL, headers=headers, json={'username': target_user}, proxies=proxy, timeout=4)
            
            if r.status_code == 200:
                is_taken = r.json().get("taken")
                if is_taken:
                    print(Fore.RED + f'[TAKEN] {target_user}')
                else:
                    print(Fore.GREEN + f'[AVAILABLE] {target_user}')
                    send_webhook_async(target_user)
                    with file_lock:
                        with open('found.txt', 'a') as f: 
                            f.write(f"{target_user}\n")
            
            elif r.status_code == 429:
                retry_after = r.json().get('retry_after', 3)
                print(Fore.YELLOW + f'[!] Rate Limited on proxy/IP. Waiting {retry_after}s...')
                time.sleep(retry_after + 0.3)
                
            elif r.status_code in [401, 403]:
                print(Fore.WHITE + f'[INVALID TOKEN] Token expired or locked. Skipping...')
                time.sleep(0.3)
                
        except requests.exceptions.ProxyError:
            print(Fore.RED + f'[Proxy Error] Changing proxy...')
            time.sleep(0.1)
        except:
            time.sleep(0.5)

        time.sleep(delay + random.uniform(0.01, 0.04))

def main():
    global webhook_url, mode_choice, user_len, delay
    cls()
    print(BANNER)
    print(Fore.RED + "                    --- Ashbah / Souls ---\n" + Fore.RESET)
    
    # تحميل البروكسيات قبل بدء العمل
    load_proxies()
    print("")
    
    webhook_url = input(Fore.CYAN + "Enter Discord Webhook (Enter to skip): ").strip()
    
    print(Fore.WHITE + "\nSelect Mode:")
    print(Fore.YELLOW + "1. Random")
    print(Fore.YELLOW + "2. Ashbah (. or _)")
    print(Fore.YELLOW + "3. Double Characters (e.g. aab1, 7xx9)")
    mode_choice = input(Fore.CYAN + "Choice (1, 2 or 3) [Default 1]: ") or "1"
    
    try:
        user_len = int(input(Fore.CYAN + "Enter length (e.g. 4) [Default 4]: ") or 4)
        delay = float(input(Fore.CYAN + "Delay per thread (sec) [Default 0.02]: ") or 0.02)
    except:
        user_len, delay = 4, 0.02

    cls()
    print(BANNER)
    print(Fore.RED + "--- Checking started with turbo mode and 12 threads! ---\n" + Fore.RESET)

    with ThreadPoolExecutor(max_workers=12) as executor:
        for _ in range(12):
            executor.submit(check_worker)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(Fore.RED + f"\n🛑 An error occurred: {e}")
        input("\nPress any key to exit...")
