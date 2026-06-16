from moviepy.video.fx import FadeIn


def animate_card(clip, duration=1.0):
    """
    Slide up + fade in animation
    """

    w, h = clip.size

    def position(t):
        # start from lower position → move up
        start_y = h
        end_y = 0

        progress = min(t / duration, 1)

        y = start_y - (start_y - end_y) * progress

        return ("center", y)

    clip = clip.with_position(position)

    # ✅ fade in
    clip = clip.with_effects([FadeIn(duration)])

    return clip