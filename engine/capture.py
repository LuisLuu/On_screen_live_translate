# engine/capture.py
import mss
import numpy as np

def capture_region(region):
    """
    Grabs pixels from a specific screen region.
    Returns: A numpy array (OpenCV style) which EasyOCR loves.
    """
    with mss.mss() as sct:
        # Grab the pixels
        screenshot = sct.grab(region)
        
        # Convert raw pixels to an RGB numpy array
        # EasyOCR needs RGB, mss gives BGRA
        img = np.array(screenshot)
        img = img[:, :, :3]  # Drop the Alpha channel
        
        return img