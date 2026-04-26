# main.py
import config
from engine.capture import capture_region
from engine.ocr import detect_text
from engine.translate import translate_text

def run_once():
    print("🚀 Taking a snapshot...")
    
    # 1. Capture
    img = capture_region(config.CAPTURE_ZONE)
    
    # 2. OCR
    print("🔍 Scanning for Japanese text...")
    results = detect_text(img)
    
    # 3. Process and Translate
    if not results:
        print("❌ No text detected in the capture zone.")
        return

    for (bbox, text, prob) in results:
        print(f"\n--- Result ({prob*100:.2f}% Confidence) ---")
        print(f"Original: {text}")
        
        translation = translate_text(text, config.SOURCE_LANG, config.TARGET_LANG)
        print(f"English: {translation}")

if __name__ == "__main__":
    run_once()