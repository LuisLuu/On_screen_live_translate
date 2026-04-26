# main.py
import config
from ui.selector import AreaSelector  # Don't forget the import!
from engine.capture import capture_region
from engine.ocr import detect_text
from engine.translate import translate_text

def run_translator():
    # 1. Ask user to sketch the area
    print("🎨 Drag a box over the Japanese text (Press Esc to cancel)")
    selector = AreaSelector()
    region = selector.get_selection()

    if not region:
        print("❌ Selection cancelled.")
        return
    
    print(f"🚀 Snapshot taken at {region}")
    
    # 2. Capture the region
    img = capture_region(region)
    
    # 3. OCR (The missing step in your snippet!)
    print("🔍 Scanning for Japanese text...")
    results = detect_text(img)

    # 4. Process and Translate
    if not results:
        print("❌ No text detected in the capture zone.")
        return

    for (bbox, text, prob) in results:
        print(f"\n--- Result ({prob*100:.2f}% Confidence) ---")
        print(f"Original: {text}")
        
        translation = translate_text(text, config.SOURCE_LANG, config.TARGET_LANG)
        print(f"English: {translation}")

if __name__ == "__main__":
    run_translator() # Call the correct function name