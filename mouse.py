import pyautogui
import time
import random
import win32api
import win32con

# ============================================
# USE MOUSE CLICKS INSTEAD OF KEYBOARD
# ============================================
TARGET_RGB = (72, 54, 32)  # Your color
TOLERANCE = 35
COOLDOWN = 0.3
# ============================================

def human_like_click():
    """Click that looks like a human"""
    # Get current position
    x, y = pyautogui.position()
    
    # Slight random offset (looks natural)
    x += random.randint(-2, 2)
    y += random.randint(-2, 2)
    win32api.SetCursorPos((x, y))
    
    # Random delay before click
    time.sleep(random.uniform(0.02, 0.1))
    
    # Click down
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    
    # Random hold duration (human holds click for varying times)
    time.sleep(random.uniform(0.02, 0.15))
    
    # Click up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    
    # Random delay after click
    time.sleep(random.uniform(0.02, 0.08))

print("🔴 WATCHING FOR COLOR - Clicking when found")
print("Press Ctrl+C to stop\n")

touches = 0
on_target = False
last_click = 0

try:
    while True:
        x, y = pyautogui.position()
        r, g, b = pyautogui.pixel(x, y)
        
        # Check if color matches
        tr, tg, tb = TARGET_RGB
        if (abs(r - tr) <= TOLERANCE and 
            abs(g - tg) <= TOLERANCE and 
            abs(b - tb) <= TOLERANCE):
            
            if not on_target and (time.time() - last_click) >= COOLDOWN:
                touches += 1
                on_target = True
                last_click = time.time()
                
                print(f"\n🎯 FOUND! #{touches} at ({x},{y})")
                
                # HUMAN-LIKE CLICK
                human_like_click()
                print(f"🖱️ Clicked!")
                
        else:
            on_target = False
            
        time.sleep(0.05)
        
except KeyboardInterrupt:
    print(f"\n✅ Stopped! Clicked {touches} times")