from moviepy import CompositeVideoClip, TextClip, ColorClip, vfx

from engine.renderer.clip_normalizer import normalize_clip
from engine.renderer.image_loader import load_image_clip
from moviepy.video.fx import FadeIn, FadeOut, Resize


def get_end_card():
    duration = 5.0

    # Base image
    clip = load_image_clip("assets/images/journey-end-card.png", duration=duration)
    
    clip = clip.with_effects([Resize(lambda t: 1 + 0.05 * smoothstep(t / duration))])

    clip = normalize_clip(clip)

    # ✅ Slight vignette overlay (professional look)
    vignette = ColorClip(size=clip.size, color=(0, 0, 0), duration=duration)
    vignette = vignette.with_opacity(0.25)


    # ✅ Combine everything
    final = CompositeVideoClip([clip, vignette])

    # ✅ Smooth fade in/out for entire clip
    
    final = final.with_effects([
        FadeIn(0.8),
        FadeOut(1.0)
    ])


    return final


# Helper easing function (more cinematic than linear zoom)
def smoothstep(x):
    return x * x * (3 - 2 * x)