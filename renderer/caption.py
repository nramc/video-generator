from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, TextClip, CompositeVideoClip
import numpy as np    

def add_title_overlay(clip, text):
    w, h = clip.size

    # ✅ create transparent image
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ✅ safe default font
    # font = ImageFont.load_default()

    font = ImageFont.truetype("Arial.ttf",55)


    # ✅ measure text
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    # ✅ center horizontally, near bottom
    x = (w - text_w) // 2
    y = int(h * 0.75)

    # ✅ background box
    padding = 25
    draw.rectangle(
        [
            x - padding,
            y - padding,
            x + text_w + padding,
            y + text_h + padding
        ],
        fill=(52, 89, 230, 200)
    )

    # ✅ draw text
    draw.text((x, y), text, font=font, fill=(255, 255, 255, 255))

    # ✅ shadow
    draw.text((x+2, y+2), text, font=font, fill=(0, 0, 0, 150))
    draw.text((x, y), text, font=font, fill=(255, 255, 255))



    # ✅ convert to clip
    txt_clip = ImageClip(np.array(img)).with_duration(clip.duration)

    return CompositeVideoClip([clip, txt_clip])