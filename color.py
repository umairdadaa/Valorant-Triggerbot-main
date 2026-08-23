import pyautogui
import logging
import time
from PIL import ImageGrab

# Setup simple logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)

def is_red(rgb):
    """Check if RGB color is red"""
    r, g, b = rgb
    return r > 200 and g < 100 and b < 100  # Red threshold

def monitor_mouse():
    """Monitor mouse position and log when touching red"""
    print("\n" + "="*50)
    print("🔴 RED DETECTOR - Move your mouse")
    print("Press Ctrl+C to stop")
    print("="*50 + "\n")
    
    last_red = False
    red_count = 0
    
    while True:
        try:
            # Get mouse position
            x, y = pyautogui.position()
            
            # Get pixel color at mouse position
            img = ImageGrab.grab(bbox=(x, y, x+1, y+1))
            rgb = img.getpixel((0, 0))
            
            # Check if red
            if is_red(rgb):
                if not last_red:  # Only log once when entering red
                    red_count += 1
                    logger.warning(f"🔴 TOUCHED RED at ({x}, {y}) - RGB: {rgb}")
                    print(f"🔥 RED! ({x}, {y}) - RGB: {rgb}")
                    last_red = True
            else:
                if last_red:
                    logger.info(f"✅ Left red at ({x}, {y})")
                    last_red = False
                    
            time.sleep(0.1)  # Check 10 times per second
            
        except KeyboardInterrupt:
            print(f"\n\n🛑 Stopped! Touched red {red_count} times")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            time.sleep(0.5)

if __name__ == "__main__":
    monitor_mouse()