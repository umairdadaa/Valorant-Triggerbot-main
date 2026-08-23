import pyautogui
import time
import sys

# ============================================
# CONFIGURATION - Change these as needed
# ============================================
TARGET_HEX = "#FF0000"  # Change this to any hex color
KEY_TO_PRESS = "c"      # Change "c" to "t" or any key
TOLERANCE = 40          # How close the color needs to be (0-255)
COOLDOWN = 0.3          # Seconds between key presses
# ============================================

def hex_to_rgb(hex_code):
    """Convert hex to RGB tuple"""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([c*2 for c in hex_code])
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

print("\n" + "="*60)
print(f"🔴 DETECTING: {TARGET_HEX}")
print(f"   Will press: '{KEY_TO_PRESS.upper()}' when detected")
print("   Move mouse over the color")
print("   Press Ctrl+C to stop")
print("="*60 + "\n")

# Convert target hex to RGB
target_rgb = hex_to_rgb(TARGET_HEX)
tr, tg, tb = target_rgb

# Variables
touches = 0
on_target = False
last_press = 0

try:
    while True:
        # Get mouse position and color
        x, y = pyautogui.position()
        r, g, b = pyautogui.pixel(x, y)
        
        # Check if color matches target (within tolerance)
        if (abs(r - tr) <= TOLERANCE and 
            abs(g - tg) <= TOLERANCE and 
            abs(b - tb) <= TOLERANCE):
            
            if not on_target and (time.time() - last_press) >= COOLDOWN:
                touches += 1
                on_target = True
                last_press = time.time()
                
                hex_found = rgb_to_hex((r, g, b))
                print(f"\n🔴 TOUCHED! Target: {TARGET_HEX} | Found: {hex_found} at ({x},{y}) [#{touches}]")
                
                # Press the key
                pyautogui.press(KEY_TO_PRESS)
                print(f"⌨️ Pressed '{KEY_TO_PRESS.upper()}'")
                
        else:
            on_target = False
        
        time.sleep(0.05)  # Check 20 times per second
        
except KeyboardInterrupt:
    print(f"\n\n✅ Stopped! Pressed '{KEY_TO_PRESS.upper()}' {touches} times")
    sys.exit()
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("Make sure you have: pip install pyautogui")
    sys.exit()