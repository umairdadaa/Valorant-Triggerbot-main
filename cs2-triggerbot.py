# Made by im-razvan - CS2 TriggerBot W/O Memory Writing
import pymem, pymem.process, keyboard, time, os
from pynput.mouse import Controller, Button
from win32gui import GetWindowText, GetForegroundWindow
from offsets import *

mouse = Controller()
client = Client()

dwEntityList = client.offset('dwEntityList')
dwLocalPlayerPawn = client.offset('dwLocalPlayerPawn')
m_iIDEntIndex = client.get('C_CSPlayerPawn', 'm_iIDEntIndex')
m_iTeamNum = client.get('C_BaseEntity', 'm_iTeamNum')
m_iHealth = client.get('C_BaseEntity', 'm_iHealth')

def is_capslock_on():
    return keyboard.is_pressed('caps lock')

def main():
    print(f"[-] TriggerBot started.")
    print(f"[-] Trigger: Caps Lock (ON = active, OFF = inactive)")
    print(f"[-] Mode: FAST - Instant shooting")
    print(f"[-] Press CTRL+C to stop")
    
    try:
        pm = pymem.Pymem("cs2.exe")
        client = pymem.process.module_from_name(pm.process_handle, "client.dll").lpBaseOfDll
    except:
        os.system("cls") if os.name == "nt" else os.system("clear")
        print("Please open CS2!")
        exit()
    
    while True:
        try:
            if not GetWindowText(GetForegroundWindow()) == "Counter-Strike 2":
                time.sleep(0.1)
                continue

            if is_capslock_on():
                player = pm.read_longlong(client + dwLocalPlayerPawn)
                entityId = pm.read_int(player + m_iIDEntIndex)

                if entityId > 0:
                    entList = pm.read_longlong(client + dwEntityList)
                    entEntry = pm.read_longlong(entList + 0x8 * (entityId >> 9) + 0x10)
                    entity = pm.read_longlong(entEntry + 120 * (entityId & 0x1FF))

                    entityTeam = pm.read_int(entity + m_iTeamNum)
                    playerTeam = pm.read_int(player + m_iTeamNum)

                    if entityTeam != playerTeam:
                        entityHp = pm.read_int(entity + m_iHealth)
                        if entityHp > 0:
                            mouse.press(Button.left)
                            mouse.release(Button.left)
            else:
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            print("\n[-] TriggerBot stopped.")
            break
        except:
            pass

if __name__ == '__main__':
    main()
