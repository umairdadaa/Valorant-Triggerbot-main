# CS2 TriggerBot - WORKING VERSION (Based on your working code)
import subprocess
import sys
import os

# ===== AUTO-INSTALL DEPENDENCIES =====
required_packages = ['pymem', 'pywin32', 'requests']

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

# Check dependencies before importing anything
if not check_and_install_dependencies():
    print("[!] Failed to install dependencies. Please install them manually.")
    input("Press Enter to exit...")
    sys.exit(1)

# Now import everything
import pymem, pymem.process, time, threading
import win32api, win32con
from requests import get as g

# ===== OFFSET SYSTEM INTEGRATED =====
class Client:
    def __init__(self):
        try:
            print("[*] Downloading latest offsets...")
            self.offsets = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/offsets.json').json()
            self.clientdll = g('https://raw.githubusercontent.com/a2x/cs2-dumper/main/output/client_dll.json').json()
            print("[+] Offsets downloaded successfully!")
        except Exception as e:
            print(f'[!] Unable to get offsets: {e}')
            print('[!] Check your internet connection.')
            exit()
    
    def offset(self, a):
        try:
            return self.offsets['client.dll'][a]
        except Exception as e:
            print(f'[!] Offset {a} not found: {e}')
            exit()
    
    def get(self, a, b):
        try:
            return self.clientdll['client.dll']['classes'][a]['fields'][b]
        except Exception as e:
            print(f'[!] Unable to get {a}, {b}: {e}')
            exit()

# Initialize offsets
client = Client()

# Get all needed offsets
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
                print("[+] TriggerBot ENABLED")
            elif user_input == "0":
                trigger_active = False
                print("[-] TriggerBot DISABLED")
            else:
                print("[!] Invalid input. Use 1 for ON, 0 for OFF")
        except:
            pass

def shoot():
    """Use win32api for reliable shooting in CS2"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.001)  # Tiny delay for reliability
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

def main():
    global trigger_active
    
    print("=" * 50)
    print("CS2 TriggerBot - WORKING VERSION")
    print("=" * 50)
    print("[+] Offsets loaded:")
    print(f"    dwEntityList: {hex(dwEntityList)}")
    print(f"    dwLocalPlayerPawn: {hex(dwLocalPlayerPawn)}")
    print(f"    m_iIDEntIndex: {hex(m_iIDEntIndex)}")
    print(f"    m_iTeamNum: {hex(m_iTeamNum)}")
    print(f"    m_iHealth: {hex(m_iHealth)}")
    print("=" * 50)
    print("Type 1 to enable, 0 to disable")
    print("Press CTRL+C to stop")
    print("=" * 50)
    
    try:
        pm = pymem.Pymem("cs2.exe")
        client_base = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
        print(f"[+] CS2 found! client.dll base: {hex(client_base)}")
    except Exception as e:
        os.system("cls") if os.name == "nt" else os.system("clear")
        print("[!] ERROR: CS2 is not running!")
        print(f"[!] Error: {e}")
        print("[!] Please open CS2 and try again.")
        input("Press Enter to exit...")
        exit()
    
    # Start input listener in a separate thread
    input_thread = threading.Thread(target=input_listener, daemon=True)
    input_thread.start()
    
    print("[+] Ready! Type 1 to enable, 0 to disable")
    print("-" * 50)
    
    while True:
        try:
            if trigger_active:
                try:
                    # Read player
                    player = pm.read_longlong(client_base + dwLocalPlayerPawn)
                    
                    if player == 0:
                        time.sleep(0.05)
                        continue
                    
                    # Read entity ID (who you're aiming at)
                    entityId = pm.read_int(player + m_iIDEntIndex)

                    if entityId > 0:
                        # Get entity from list
                        entList = pm.read_longlong(client_base + dwEntityList)
                        entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                        entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                        # Check teams
                        entityTeam = pm.read_int(entity + m_iTeamNum)
                        playerTeam = pm.read_int(player + m_iTeamNum)

                        # If enemy
                        if entityTeam != playerTeam:
                            # Check health
                            entityHp = pm.read_int(entity + m_iHealth)
                            if entityHp > 0:
                                # SHOOT using win32api (reliable)
                                shoot()
                    else:
                        time.sleep(0.01)
                        
                except Exception as e:
                    # Silently handle errors
                    time.sleep(0.05)
            else:
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[-] TriggerBot stopped.")
            break
        except Exception as e:
            time.sleep(0.1)

if __name__ == '__main__':
    main()
