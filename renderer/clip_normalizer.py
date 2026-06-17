from moviepy import CompositeVideoClip, ImageClip
from PIL import Image, ImageFilter, ImageOps
import numpy as np


def normalize_clip(clip, resolution=(1280, 720)):
    target_w, target_h = resolution
    w, h = clip.size

    # scale clip
    scale = min(target_w / w, target_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    clip = clip.resized((new_w, new_h))

    # ✅ blurred background
    frame = clip.get_frame(0)
    img = Image.fromarray(frame)
    img = ImageOps.exif_transpose(img)
    img = img.resize(resolution)

    img = img.filter(ImageFilter.GaussianBlur(25))

    bg = ImageClip(np.array(img)).with_duration(clip.duration)

    clip = clip.with_position(("center", "center"))

    return CompositeVideoClip([bg, clip])