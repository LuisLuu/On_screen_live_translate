# engine/ocr.py
import easyocr

# Initialize the reader OUTSIDE the function to keep it fast
# 'ja' for Japanese, 'en' for English
reader = easyocr.Reader(['ja', 'en'], gpu=False) # Set to True if you have a GPU

def detect_text(image_np):
    """
    Scans the image for text.
    Returns: List of results containing (box, text, confidence)
    """
    results = reader.readtext(image_np)
    return results