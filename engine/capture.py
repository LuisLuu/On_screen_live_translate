# engine/capture.py
import mss
import numpy as np
import cv2

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

def blur_image(image_np, strength=15):
    """
    Applies a Gaussian blur to the captured pixels.
    """
    # strength must be an odd number
    return cv2.GaussianBlur(image_np, (strength, strength), 0)