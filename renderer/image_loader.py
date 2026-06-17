
from PIL import Image, ImageOps
from moviepy import ImageClip
import numpy as np


def load_image_clip(path, duration):
    img = Image.open(path)

    # ✅ FIX: apply EXIF orientation
    img = ImageOps.exif_transpose(img)

    return ImageClip(np.array(img), duration=duration)

