import keyboard
import time
import threading
import numpy as np
from ui.selector import AreaSelector
from engine.capture import capture_region
from engine.ocr import detect_text
from engine.translate import translate_text

# Global state
is_running = False
current_region = None
last_image = None

def live_translate_loop():
    global is_running, current_region, last_image
    
    print("🛰️  Live mode started. Looking...")
    
    while is_running:
        if current_region:
            # 1. Capture the pixels
            img = capture_region(current_region)
            
            # 2. Delta Check: Did the screen actually change?
            if last_image is not None:
                # We calculate the "Difference" between frames
                diff = np.sum(np.abs(img.astype(np.float32) - last_image.astype(np.float32)))
                if diff < 100000: # Threshold: pixels are basically the same
                    time.sleep(0.5) # Wait half a second and try again
                    continue
            
            last_image = img
            
            # 3. OCR and Translate
            results = detect_text(img)
            for (bbox, text, prob) in results:
                if prob > 0.5: # Only translate confident hits
                    trans = translate_text(text)
                    print(f"[{time.strftime('%H:%M:%S')}] {text} -> {trans}")
            
            # Small delay to prevent API spamming
            time.sleep(1.0) 

def toggle_translator():
    global is_running, current_region
    
    if not is_running:
        # Step 1: Selection
        print("\n🎨 Select the 'Live Zone'...")
        selector = AreaSelector()
        current_region = selector.get_selection()
        
        if current_region:
            is_running = True
            # Start the loop in a separate thread so the hotkey still works
            threading.Thread(target=live_translate_loop, daemon=True).start()
    else:
        print("🛑 Stopping Live mode...")
        is_running = False

def main():
    print("🚀 On-Screen Trans is READY.")
    print("👉 Press: Ctrl+Alt+S to Start/Stop Live Translation")
    print("👉 Press: Esc to Kill App")

    keyboard.add_hotkey('ctrl+alt+s', toggle_translator)
    keyboard.wait('esc')

if __name__ == "__main__":
    main()