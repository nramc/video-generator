from moviepy import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip
from moviepy.video.fx import CrossFadeIn

from renderer.caption import add_title_overlay
from renderer.clip_normalizer import normalize_clip
from utils.effects_utils import ken_burns_effect


def render_video(timeline, music_path, output_path, title=None, subtitle=None):
    clips = []

    for i, item in enumerate(timeline):

        if item["type"] == "image":
            clip = ImageClip(item["file"], duration=max(2, item["duration"]))

        elif item["type"] == "video":
            clip = safe_subclip(item["file"], item.get("start", 0), item.get("end"))
        else:
            continue
        
        clip = normalize_clip(clip)
        # Apply Ken Burns ONLY to images
        if item["type"] == "image":
            clip = ken_burns_effect(clip)

        # ✅ Apply title only to first clip
        if i == 0 and title:
            clip = add_title_overlay(clip, title, subtitle)

        clips.append(clip)

    # Add transitions between clips
    clips = [clips[0]] + [clip.with_effects([CrossFadeIn(1)]) for clip in clips[1:]]


    video = concatenate_videoclips(clips, method="compose")

    # Add audio
    audio = AudioFileClip(music_path).subclipped(0, video.duration)


    final = video.with_audio(audio)

    final.write_videofile(output_path, fps=24)



def safe_subclip(file, start=None, end=None):
    clip = VideoFileClip(file)

    duration = clip.duration

    start = start or 0
    end = end or duration

    # ✅ Clamp values
    start = max(0, start)
    end = min(end, duration)

    # ✅ Fix invalid ranges
    if start >= end:
        return clip

    return clip.subclipped(start, end)
