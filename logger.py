import pyautogui
import logging
import time

# ============================================
# CONFIGURATION - Change this hex value to detect different colors!
# ============================================
TARGET_HEX = "#FF0000"  # Change this to any hex color you want to detect
# Examples: "#FF0000" (red), "#00FF00" (green), "#0000FF" (blue), "#FFFF00" (yellow)
# ============================================

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def hex_to_rgb(hex_code):
    """Convert hex code to RGB tuple"""
    hex_code = hex_code.lstrip('#')
    if len(hex_code) == 3:
        hex_code = ''.join([c*2 for c in hex_code])
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    """Convert RGB to hex code"""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}".upper()

def is_color_match(rgb, target_rgb, tolerance=30):
    """Check if RGB matches target RGB within tolerance"""
    r, g, b = rgb
    tr, tg, tb = target_rgb
    return (abs(r - tr) <= tolerance and 
            abs(g - tg) <= tolerance and 
            abs(b - tb) <= tolerance)

def monitor_mouse():
    """Monitor mouse and log when target hex color is touched"""
    target_rgb = hex_to_rgb(TARGET_HEX)
    
    print("\n" + "="*60)
    print(f"🔴 DETECTING HEX: {TARGET_HEX}")
    print(f"   RGB: {target_rgb}")
    print("   Move your mouse over the target color")
    print("   Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    last_was_target = False
    touches = 0
    
    while True:
        try:
            # Get mouse position
            x, y = pyautogui.position()
            
            # Get pixel color
            rgb = pyautogui.pixel(x, y)
            hex_code = rgb_to_hex(rgb)
            
            # Check if matches target
            if is_color_match(rgb, target_rgb):
                if not last_was_target:
                    touches += 1
                    last_was_target = True
                    r, g, b = rgb
                    logger.warning(f"🔴 TOUCHED {TARGET_HEX}! Found: {hex_code} RGB:({r},{g},{b}) at ({x},{y}) [#{touches}]")
                    print(f"🔥 {hex_code} matched {TARGET_HEX} at ({x}, {y})")
            else:
                if last_was_target:
                    last_was_target = False
                    logger.info(f"✅ Left target at ({x}, {y})")
            
            time.sleep(0.05)
            
        except KeyboardInterrupt:
            print(f"\n\n🛑 Stopped! Touched {TARGET_HEX} {touches} times")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(0.5)

if __name__ == "__main__":
    monitor_mouse()