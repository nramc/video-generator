from moviepy import CompositeVideoClip, ImageClip
from PIL import Image, ImageDraw, ImageFont
import numpy as np

from renderer.animation import animate_card


def add_title_overlay(clip, title, subtitle=None):
    w, h = clip.size

    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # ✅ fonts
    title_font = ImageFont.truetype(
        "assets/fonts/dejavu-sans/DejaVuSans-Bold.ttf",
        int(h * 0.06)
    )
    subtitle_font = ImageFont.truetype(
        "assets/fonts/dejavu-sans/DejaVuSans-Bold.ttf",
        int(h * 0.035)
    )

    # ✅ measure title
    t_bbox = draw.textbbox((0, 0), title, font=title_font)
    t_w = t_bbox[2] - t_bbox[0]
    t_h = t_bbox[3] - t_bbox[1]

    # ✅ measure subtitle
    if subtitle:
        s_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
        s_w = s_bbox[2] - s_bbox[0]
        s_h = s_bbox[3] - s_bbox[1]
    else:
        s_w = s_h = 0

    # ✅ block dimensions
    max_w = max(t_w, s_w)
    total_h = t_h + (s_h + 10 if subtitle else 0)

    x = (w - max_w) // 2
    y = int(h * 0.70)

    padding = 25

    # ✅ background (your theme color)
    #draw.rectangle([x - padding, y - padding, x + max_w + padding, y + total_h + padding ], fill=(52, 89, 230, 200))

    # shadow (depth)
    draw.rounded_rectangle(
        [
            x - padding + 4,
            y - padding + 4,
            x + max_w + padding + 4,
            y + total_h + padding + 4
        ],
        radius=20,
        fill=(0, 0, 0, 100)
    )

    # main card
    draw.rounded_rectangle(
        [
            x - padding,
            y - padding,
            x + max_w + padding,
            y + total_h + padding
        ],
        radius=20,
        fill=(52, 89, 230, 255)
    )

    # subtle glow outline
    draw.rounded_rectangle(
        [x - padding, y - padding, x + max_w + padding, y + total_h + padding],
        radius=20,
        outline=(120, 160, 255, 80),
        width=2
    )


    # ✅ TITLE (white + shadow)
    tx = (w - t_w) // 2
    draw.text((tx + 2, y + 2), title, font=title_font, fill=(0, 0, 0, 150))
    draw.text((tx, y), title, font=title_font, fill=(255, 255, 255, 255))

    # ✅ SUBTITLE
    if subtitle:
        sy = y + t_h + 10
        sx = (w - s_w) // 2

        draw.text((sx + 2, sy + 2), subtitle, font=subtitle_font, fill=(0, 0, 0, 120))
        draw.text((sx, sy), subtitle, font=subtitle_font, fill=(235, 235, 235, 255))

    txt_clip = ImageClip(np.array(img)).with_duration(min(3, clip.duration))

    animated = animate_card(txt_clip, duration=0.8)

    return CompositeVideoClip([clip, animated])
