# engine/translate.py
from deep_translator import GoogleTranslator

def translate_text(text, src='ja', dest='en'):
    """
    Translates text using Deep Translator (Sync).
    """
    if not text.strip():
        return ""
        
    try:
        # No coroutines, just straight translation
        translated = GoogleTranslator(source=src, target=dest).translate(text)
        return translated
    except Exception as e:
        print(f"Translation Error: {e}")
        return "[Translation Failed]"