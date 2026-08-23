import pyautogui
import logging
import time
import sys

# ============================================
# CONFIGURATION - Change these defaults
# ============================================
TARGET_HEX = "#FF0000"  # Default hex color
KEY_TO_PRESS = "c"      # Default key - Change to "t" or any key
COOLDOWN = 0.5
TOLERANCE = 30
# ============================================

# Override with command line arguments if provided
if len(sys.argv) > 1:
    TARGET_HEX = sys.argv[1]
if len(sys.argv) > 2:
    KEY_TO_PRESS = sys.argv[2].lower()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger()

def press_key():
    pyautogui.press(KEY_TO_PRESS)
    print(f"⌨️ Pressed '{KEY_TO_PRESS.upper()}'")

def monitor_mouse():
    target = tuple(int(TARGET_HEX.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    tr, tg, tb = target
    
    print(f"\n🔴 Detecting {TARGET_HEX} -> Pressing '{KEY_TO_PRESS.upper()}'")
    print("Press Ctrl+C to stop\n")
    
    touches = 0
    on_target = False
    last_press = 0
    
    while True:
        try:
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            
            if abs(r-tr) <= TOLERANCE and abs(g-tg) <= TOLERANCE and abs(b-tb) <= TOLERANCE:
                if not on_target and (time.time() - last_press) >= COOLDOWN:
                    touches += 1
                    on_target = True
                    last_press = time.time()
                    hex_found = f"#{r:02x}{g:02x}{b:02x}".upper()
                    logger.warning(f"🔴 FOUND {TARGET_HEX}! Detected: {hex_found}")
                    press_key()
            else:
                on_target = False
                
            time.sleep(0.05)
            
        except KeyboardInterrupt:
            print(f"\n✅ Found {TARGET_HEX} {touches} times")
            print(f"⌨️ Pressed '{KEY_TO_PRESS.upper()}' {touches} times")
            break

if __name__ == "__main__":
    monitor_mouse()