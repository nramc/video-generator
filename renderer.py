from moviepy import ImageClip, VideoFileClip, concatenate_videoclips, AudioFileClip
from utils import normalize_clip, ken_burns_effect
from moviepy.video.fx import CrossFadeIn


def render_video(timeline, music_path, output_path):
    clips = []

    for item in timeline:
        if item["type"] == "image":
            clip = ImageClip(item["file"], duration=item["duration"])

        elif item["type"] == "video":
            clip = VideoFileClip(item["file"]).subclipped(
                item.get("start", 0),
                item.get("end")
            )

        clip = normalize_clip(clip)
        # Apply Ken Burns ONLY to images
        if item["type"] == "image":
            clip = ken_burns_effect(clip)

        clips.append(clip)

    # Add transitions between clips
    clips = [clips[0]] + [clip.with_effects([CrossFadeIn(1)]) for clip in clips[1:]]


    video = concatenate_videoclips(clips, method="compose")

    # Add audio
    audio = AudioFileClip(music_path).subclipped(0, video.duration)


    final = video.with_audio(audio)

    final.write_videofile(output_path, fps=24)