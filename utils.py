def normalize_clip(clip, resolution=(1280, 720)):
    return clip.resized(resolution)

def ken_burns_zoom(clip, zoom_factor=1.1):
    """
    Applies a slow zoom-in effect.
    zoom_factor > 1 means zoom in
    """
    duration = clip.duration

    def zoom(t):
        return 1 + (zoom_factor - 1) * (t / duration)

    return clip.resized(lambda t: zoom(t))

def ken_burns_effect(clip, zoom_factor=1.1):
    duration = clip.duration
    w, h = clip.size

    from PIL import Image
    import numpy as np

    original_frame = clip.get_frame(0)

    def frame_func(t):
        progress = t / duration

        scale = 1 + (zoom_factor - 1) * progress

        new_w = int(w * scale)
        new_h = int(h * scale)

        img = Image.fromarray(original_frame)
        img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # center crop
        x = (new_w - w) // 2
        y = (new_h - h) // 2

        img = img.crop((x, y, x + w, y + h))

        return np.array(img)

    return clip.with_updated_frame_function(frame_func)
