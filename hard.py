import pyautogui
import time
import sys
import ctypes
from ctypes import wintypes

# ============================================
# CONFIGURATION - Change these as needed
# ============================================
TARGET_HEX = "#FF0000"  # Hex color to detect
KEY_TO_PRESS = "c"      # Key to press (hardware-level)
TOLERANCE = 40          # Color matching tolerance
COOLDOWN = 0.3          # Seconds between presses
# ============================================

# --- Hardware-level key press using Windows SendInput ---
# These are the virtual key codes for common keys
VK_CODES = {
    'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
    'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
    'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
    'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
    'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
    '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
    '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
    'space': 0x20, 'enter': 0x0D, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
}

# Define the Input structures for SendInput
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong), ("wParamL", ctypes.c_short), ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long), ("dy", ctypes.c_long), ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput), ("mi", MouseInput), ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

def press_key_hardware(key):
    """Press a key at the hardware level using SendInput (works in games)"""
    if key not in VK_CODES:
        print(f"⚠️ No virtual key code for '{key}'")
        return
    
    vk_code = VK_CODES[key]
    
    # Key Down
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vk_code, 0, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    
    time.sleep(0.02)  # Small delay between down and up
    
    # Key Up
    ii_ = Input_I()
    ii_.ki = KeyBdInput(vk_code, 0, 0x0002, 0, ctypes.pointer(extra))  # KEYEVENTF_KEYUP = 0x0002
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# --- Color detection (same as before) ---
def hex_to_rgb(hex_code):
    """Convert hex to RGB tuple"""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([c*2 for c in hex_code])
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

# --- Main Loop ---
print("\n" + "="*60)
print(f"🔴 DETECTING: {TARGET_HEX}")
print(f"   Will press: '{KEY_TO_PRESS.upper()}' (HARDWARE-LEVEL)")
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
                
                # Press the key at hardware level
                press_key_hardware(KEY_TO_PRESS)
                print(f"⌨️ Pressed '{KEY_TO_PRESS.upper()}' (Hardware)")
                
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