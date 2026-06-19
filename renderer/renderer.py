from moviepy import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip
from moviepy.video.fx import CrossFadeIn

from renderer.caption import add_title_overlay
from renderer.clip_normalizer import normalize_clip
from renderer.image_loader import load_image_clip
from renderer.journey_end_card import get_end_card
from utils.effects_utils import ken_burns_effect
from moviepy.audio.fx import AudioLoop



def render_video(timeline, music_path, output_path, title=None, subtitle=None):
    clips = []

    for i, item in enumerate(timeline):

        if item["type"] == "image":
            clip = load_image_clip(item["file"],duration=max(2, item["duration"]))

        elif item["type"] == "video":
            clip = safe_subclip(item["file"], item.get("start", 0), item.get("end"))
        else:
            continue
        
        clip = normalize_clip(clip)
        # Apply Ken Burns ONLY to images
        if item["type"] == "image":
            clip = ken_burns_effect(clip)

        clips.append(clip)

     # ✅ FINAL END CARD
    end_card = get_end_card()
    clips.append(end_card)

    # Add transitions between clips
    clips = [clips[0]] + [clip.with_effects([CrossFadeIn(1)]) for clip in clips[1:]]

    composed_video = concatenate_videoclips(clips, method="compose")

    # Apply title/subtitle overlay
    video = add_title_overlay(composed_video, title, subtitle)


    # Add audio
    audio = get_audio_clip(music_path, video.duration)
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

def get_audio_clip(music_path, target_duration):
    audio = AudioFileClip(music_path)

    if audio.duration < target_duration:
        audio = audio.with_effects([
            AudioLoop(duration=target_duration)
        ])
    else:
        audio = audio.subclipped(0, target_duration)

    return audio