# CS2 TriggerBot - EXACT MATCH to your working code's shooting method
import subprocess
import sys
import os

# ===== AUTO-INSTALL DEPENDENCIES =====
required_packages = ['pymem', 'pywin32', 'requests', 'colorama']

def install_package(package):
    print(f"[*] Installing {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"[+] {package} installed successfully!")
        return True
    except:
        print(f"[!] Failed to install {package}")
        return False

def check_and_install_dependencies():
    print("=" * 50)
    print("Checking dependencies...")
    print("=" * 50)
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"[+] {package} - OK")
        except ImportError:
            print(f"[-] {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print("-" * 50)
        print(f"[!] Missing {len(missing_packages)} package(s): {', '.join(missing_packages)}")
        print("[*] Installing missing packages...")
        print("-" * 50)
        
        for package in missing_packages:
            if not install_package(package):
                print(f"[!] Please manually install {package}: pip install {package}")
                return False
        
        print("-" * 50)
        print("[+] All dependencies installed successfully!")
        return True
    else:
        print("-" * 50)
        print("[+] All dependencies are installed!")
        return True

if not check_and_install_dependencies():
    print("[!] Failed to install dependencies.")
    input("Press Enter to exit...")
    sys.exit(1)

import pymem, pymem.process, time, threading, random
import win32api, win32con
from colorama import Fore, Style, init
from requests import get as g

init(autoreset=True)

# ===== OFFSETS =====
class Client:
    def __init__(self):
        try:
            print("[*] Downloading latest offsets...")
            self.offsets = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
            self.clientdll = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()
            print("[+] Offsets downloaded successfully!")
        except:
            print('[!] Unable to get offsets.')
            exit()
    
    def offset(self, a):
        try:
            return self.offsets['client.dll'][a]
        except:
            print(f'[!] Offset {a} not found.')
            exit()
    
    def get(self, a, b):
        try:
            return self.clientdll['client.dll']['classes'][a]['fields'][b]
        except:
            print(f'[!] Unable to get {a}, {b}.')
            exit()

client = Client()
dwEntityList = client.offset('dwEntityList')
dwLocalPlayerPawn = client.offset('dwLocalPlayerPawn')
m_iIDEntIndex = client.get('C_CSPlayerPawn', 'm_iIDEntIndex')
m_iTeamNum = client.get('C_BaseEntity', 'm_iTeamNum')
m_iHealth = client.get('C_BaseEntity', 'm_iHealth')

trigger_active = False

def input_listener():
    global trigger_active
    while True:
        try:
            user_input = input("Enter 1 to ON, 0 to OFF: ")
            if user_input == "1":
                trigger_active = True
                print(Fore.GREEN + "[+] TriggerBot ENABLED")
            elif user_input == "0":
                trigger_active = False
                print(Fore.RED + "[-] TriggerBot DISABLED")
            else:
                print("[!] Invalid input. Use 1 for ON, 0 for OFF")
        except:
            pass

def main():
    global trigger_active
    
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "CS2 TriggerBot - WORKING VERSION")
    print(Fore.CYAN + "=" * 50)
    print(Fore.YELLOW + f"dwEntityList: {hex(dwEntityList)}")
    print(Fore.YELLOW + f"dwLocalPlayerPawn: {hex(dwLocalPlayerPawn)}")
    print(Fore.YELLOW + f"m_iIDEntIndex: {hex(m_iIDEntIndex)}")
    print(Fore.YELLOW + f"m_iTeamNum: {hex(m_iTeamNum)}")
    print(Fore.YELLOW + f"m_iHealth: {hex(m_iHealth)}")
    print(Fore.CYAN + "=" * 50)
    print("Type 1 to enable, 0 to disable")
    print("Press CTRL+C to stop")
    print(Fore.CYAN + "=" * 50)
    
    try:
        pm = pymem.Pymem("cs2.exe")
        client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        print(Fore.GREEN + f"[+] CS2 found! base: {hex(client_base)}")
    except:
        print(Fore.RED + "[!] ERROR: CS2 is not running!")
        input("Press Enter to exit...")
        exit()
    
    input_thread = threading.Thread(target=input_listener, daemon=True)
    input_thread.start()
    
    print(Fore.GREEN + "[+] Ready!")
    print(Fore.CYAN + "-" * 50)
    
    while True:
        try:
            if trigger_active:
                try:
                    player = pm.read_longlong(client_base + dwLocalPlayerPawn)
                    
                    if player == 0:
                        time.sleep(0.05)
                        continue
                    
                    entityId = pm.read_int(player + m_iIDEntIndex)

                    if entityId > 0:
                        entList = pm.read_longlong(client_base + dwEntityList)
                        entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                        entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                        entityTeam = pm.read_int(entity + m_iTeamNum)
                        playerTeam = pm.read_int(player + m_iTeamNum)

                        if entityTeam != playerTeam:
                            entityHp = pm.read_int(entity + m_iHealth)
                            if entityHp > 0:
                                # EXACT SAME SHOOTING METHOD AS YOUR WORKING CODE
                                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                                time.sleep(0.001)
                                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                    else:
                        time.sleep(0.01)
                        
                except:
                    time.sleep(0.05)
            else:
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print(Fore.RED + "\n[-] TriggerBot stopped.")
            break
        except:
            time.sleep(0.1)

if __name__ == '__main__':
    main()
