import pyautogui
import time
import sys
import os

# Try to import hardware key libraries
try:
    import win32api
    import win32con
    HAS_WIN32 = True
except:
    HAS_WIN32 = False
    print("⚠️ pywin32 not installed. Using pyautogui (may not work in games)")
    print("   Install with: pip install pywin32\n")

# ============================================
# COLOR OPTIONS
# ============================================
COLORS = {
    "1": {
        "name": "Red (Default)",
        "hex": "#FF4655",
        "rgb": (255, 70, 85)
    },
    "2": {
        "name": "Purple (Tritanopia)",
        "hex": "#C86BFF",
        "rgb": (200, 107, 255)
    },
    "3": {
        "name": "Yellow (Deuteranopia)",
        "hex": "#FFFF00",
        "rgb": (255, 255, 0)
    },
    "4": {
        "name": "Yellow (Protanopia)",
        "hex": "#FFD700",
        "rgb": (255, 215, 0)
    }
}

# ============================================
# CONFIGURATION
# ============================================
TOLERANCE = 40          # How close the color needs to be
KEY_TO_PRESS = "c"      # Key to press when detected
COOLDOWN = 0.3          # Seconds between presses
USE_HARDWARE = True     # True = hardware key (works in games)
# ============================================

def press_key_hardware(key):
    """Hardware-level key press using win32api (works in games)"""
    if not HAS_WIN32:
        pyautogui.press(key)
        return
    
    vk_codes = {
        'a': 0x41, 'b': 0x42, 'c': 0x43, 'd': 0x44, 'e': 0x45,
        'f': 0x46, 'g': 0x47, 'h': 0x48, 'i': 0x49, 'j': 0x4A,
        'k': 0x4B, 'l': 0x4C, 'm': 0x4D, 'n': 0x4E, 'o': 0x4F,
        'p': 0x50, 'q': 0x51, 'r': 0x52, 's': 0x53, 't': 0x54,
        'u': 0x55, 'v': 0x56, 'w': 0x57, 'x': 0x58, 'y': 0x59, 'z': 0x5A,
        '0': 0x30, '1': 0x31, '2': 0x32, '3': 0x33, '4': 0x34,
        '5': 0x35, '6': 0x36, '7': 0x37, '8': 0x38, '9': 0x39,
        'space': 0x20, 'enter': 0x0D, 'shift': 0x10, 'ctrl': 0x11, 'alt': 0x12,
    }
    
    if key not in vk_codes:
        pyautogui.press(key)
        return
    
    vk = vk_codes[key]
    
    # Key down
    win32api.keybd_event(vk, 0, 0, 0)
    time.sleep(0.02)
    # Key up
    win32api.keybd_event(vk, 0, win32con.KEYEVENTF_KEYUP, 0)

def rgb_to_hex(rgb):
    """Convert RGB to hex string"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def show_menu():
    """Display color selection menu"""
    clear_screen()
    print("="*60)
    print("🎯 COLOR DETECTOR - Select a color to detect")
    print("="*60)
    print()
    
    for key, color in COLORS.items():
        # Create a colored preview (works in some terminals)
        hex_code = color['hex']
        print(f"  [{key}] {color['name']:25} {hex_code}")
    
    print()
    print("  [q] Quit")
    print("="*60)
    print()

def get_user_choice():
    """Get color selection from user"""
    while True:
        choice = input("👉 Select a color (1-4): ").strip()
        
        if choice.lower() == 'q':
            return None
        
        if choice in COLORS:
            return choice
        
        print("❌ Invalid choice. Please select 1, 2, 3, 4, or q")

def monitor_mouse(target_rgb, target_name, target_hex):
    """Main monitoring loop"""
    tr, tg, tb = target_rgb
    
    print("\n" + "="*60)
    print(f"🔴 DETECTING: {target_name}")
    print(f"   Hex: {target_hex}")
    print(f"   RGB: {target_rgb}")
    print(f"   Tolerance: {TOLERANCE}")
    print(f"   Key: '{KEY_TO_PRESS.upper()}' ({'HARDWARE' if USE_HARDWARE and HAS_WIN32 else 'SOFTWARE'})")
    print("   Move mouse over the color in your game")
    print("   Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    touches = 0
    on_target = False
    last_press = 0
    debug_counter = 0
    
    try:
        while True:
            # Get mouse position and color
            x, y = pyautogui.position()
            r, g, b = pyautogui.pixel(x, y)
            hex_found = rgb_to_hex((r, g, b))
            
            # Show debug info every 20 frames
            debug_counter += 1
            if debug_counter % 20 == 0:
                diff_r = abs(r - tr)
                diff_g = abs(g - tg)
                diff_b = abs(b - tb)
                print(f"📍 {hex_found} RGB({r:3},{g:3},{b:3}) | Diff: {diff_r+diff_g+diff_b:3}", end="\r")
            
            # Check if color matches target (within tolerance)
            color_match = (
                abs(r - tr) <= TOLERANCE and 
                abs(g - tg) <= TOLERANCE and 
                abs(b - tb) <= TOLERANCE
            )
            
            if color_match:
                if not on_target and (time.time() - last_press) >= COOLDOWN:
                    touches += 1
                    on_target = True
                    last_press = time.time()
                    
                    print(f"\n🔴 {target_name} DETECTED!")
                    print(f"   Found: {hex_found} at ({x},{y}) RGB({r},{g},{b})")
                    print(f"   Touch #{touches}")
                    
                    # Press the key
                    if USE_HARDWARE and HAS_WIN32:
                        press_key_hardware(KEY_TO_PRESS)
                        print(f"   ⌨️ Pressed '{KEY_TO_PRESS.upper()}' (HARDWARE)")
                    else:
                        pyautogui.press(KEY_TO_PRESS)
                        print(f"   ⌨️ Pressed '{KEY_TO_PRESS.upper()}' (SOFTWARE)")
                    print()
                    
            else:
                on_target = False
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print(f"\n\n✅ Stopped! Detected {target_name} {touches} times")
        print(f"   Pressed '{KEY_TO_PRESS.upper()}' {touches} times")
        sys.exit()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        time.sleep(2)
        sys.exit()

# ============================================
# MAIN PROGRAM
# ============================================
if __name__ == "__main__":
    while True:
        show_menu()
        choice = get_user_choice()
        
        if choice is None:
            print("\n👋 Goodbye!")
            sys.exit()
        
        # Get selected color
        selected = COLORS[choice]
        target_name = selected['name']
        target_hex = selected['hex']
        target_rgb = selected['rgb']
        
        # Start monitoring
        monitor_mouse(target_rgb, target_name, target_hex)
        
        # Ask if user wants to continue
        print("\n" + "="*60)
        again = input("🔄 Detect another color? (y/n): ").strip().lower()
        if again != 'y':
            print("\n👋 Goodbye!")
            break