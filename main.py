import sys
import threading
import time
import keyboard
from PyQt6.QtWidgets import QApplication
from ui.selector import AreaSelector
from ui.overlay import TranslationHUD  # Ensure this file exists!
from engine.capture import capture_region
from engine.ocr import detect_text
from engine.translate import translate_text

# 1. Global State
app = QApplication(sys.argv)
hud = None
is_running = False
current_region = None

def live_engine_logic():
    global is_running, hud, current_region
    
    print("🛰️  Engine is now scanning...")
    
    while is_running:
        if current_region and hud:
            # A. Capture
            img = capture_region(current_region)
            
            # B. OCR
            results = detect_text(img)
            
            # C. Translate & Combine
            full_translation = ""
            for (bbox, text, prob) in results:
                if prob > 0.3:  # Confidence threshold
                    translated = translate_text(text)
                    full_translation += f"{translated} "
            
            # D. Update HUD
            if full_translation.strip():
                # Note: In a 'Right Way' app, we'd use a Signal here.
                # For our speed-run, this works for now.
                hud.update_text(full_translation.strip())
            
        time.sleep(1.0)  # Breath to prevent CPU meltdown/API ban

def on_activate():
    global hud, is_running, current_region
    
    if not is_running:
        print("🎯 Selection Mode Active...")
        selector = AreaSelector()
        current_region = selector.get_selection()
        
        if current_region:
            is_running = True
            # Spawn HUD
            hud = TranslationHUD(
                current_region['left'], 
                current_region['top'], 
                current_region['width'], 
                current_region['height']
            )
            hud.show()
            
            # Kick off the logic thread
            threading.Thread(target=live_engine_logic, daemon=True).start()
    else:
        print("🛑 Stopping Translator...")
        is_running = False
        if hud:
            hud.hide()

def start_app():
    # Register the "Tripwire"
    keyboard.add_hotkey('ctrl+alt+s', on_activate)
    
    print("🚀 On-Screen Trans is RUNNING.")
    print("1. Go to your Japanese tab.")
    print("2. Press Ctrl + Alt + S to select area.")
    print("3. Press Ctrl + Alt + S again to stop.")
    
    # This keeps the PyQt window system alive
    sys.exit(app.exec())

if __name__ == "__main__":
    start_app()