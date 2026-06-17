import json
from tracemalloc import start

from moviepy import VideoFileClip
import random

from timeline.beat_detector import generate_duration_using_beats
from utils.date_utils import get_file_name_with_date



def generate_timeline_using_beats(media_files, music_path):
    durations = generate_duration_using_beats(music_path)

    timeline = build_timeline(media_files, durations)

    output_path= "output/"+ get_file_name_with_date("timeline_beat.json")
    with open(output_path, "w") as f:
        json.dump(timeline, f, indent=2)

    return timeline


def build_timeline(media_files, durations, max_video_reuse=2):
    timeline = []

    image_ext = (".jpg", ".jpeg", ".png")
    video_ext = (".mp4", ".mov", ".mkv")

    images = [f for f in media_files if f.lower().endswith(image_ext)]
    videos = [f for f in media_files if f.lower().endswith(video_ext)]

    random.shuffle(images)
    image_index = 0

    last_video_file = None
    video_usage = {}             # total seconds used
    video_count = {}             # number of times used ✅ NEW
    video_segments_used = {}

    # ✅ cache video metadata
    video_info = {}
    for f in videos:
        clip = VideoFileClip(f)
        video_info[f] = {
            "clip": clip,
            "duration": clip.duration
        }

    for duration in durations:
        duration = float(max(2.0, duration))

        # ✅ decide media type
        use_video = False
        if videos:
            if duration > 3:
                use_video = True
            if random.random() < 0.3:
                use_video = not use_video

        # ✅ IMAGE (no repetition)
        if not use_video and image_index < len(images):
            file = images[image_index]
            image_index += 1

            timeline.append({
                "type": "image",
                "file": file,
                "duration": duration
            })
            continue

        # ✅ VIDEO PATH WITH HARD LIMIT ✅
        if videos:
            weighted_pool = []

            for f in videos:
                # ✅ avoid same video consecutively
                if f == last_video_file:
                    continue

                # ✅ HARD LIMIT on reuse
                if video_count.get(f, 0) >= max_video_reuse:
                    continue

                info = video_info[f]
                video_length = info["duration"]

                current_usage = video_usage.get(f, 0)
                max_usage = video_length * 1.0  # allow reuse up to 1x duration

                remaining = max_usage - current_usage
                if remaining <= 0:
                    continue

                # ✅ weight by unused portion
                weight = remaining

                # ✅ boost videos never used
                if video_count.get(f, 0) == 0:
                    weight *= 2

                weighted_pool.append((f, weight))

            # ✅ fallback (relax rules slightly if needed)
            if not weighted_pool:
                weighted_pool = [
                    (f, 1.0)
                    for f in videos
                    if f != last_video_file
                    and video_count.get(f, 0) < max_video_reuse
                ]

            if not weighted_pool:
                break

            # ✅ weighted selection
            files = [f for f, w in weighted_pool]
            weights = [w for f, w in weighted_pool]
            file = random.choices(files, weights=weights, k=1)[0]

            info = video_info[file]
            clip_full = info["clip"]
            video_length = info["duration"]

            play_duration = duration
            max_start = max(0, video_length - play_duration)

            # ✅ smart segment selection
            attempts = 6
            best_start = 0
            best_score = -1

            used_segments = video_segments_used.get(file, [])

            for _ in range(attempts):
                candidate = random.uniform(0, max_start) if max_start > 0 else 0

                if not used_segments:
                    best_start = candidate
                    break

                min_distance = min(
                    (min(abs(candidate - s), abs(candidate - e)) for s, e in used_segments),
                    default=float("inf")
                )

                if min_distance > best_score:
                    best_score = min_distance
                    best_start = candidate

            start = best_start
            end = start + play_duration

            # ✅ update trackers
            last_video_file = file
            video_usage[file] = video_usage.get(file, 0) + duration
            video_count[file] = video_count.get(file, 0) + 1   # ✅ NEW
            video_segments_used.setdefault(file, []).append((start, end))

            timeline.append({
                "type": "video",
                "file": file,
                "start": start,
                "end": end
            })

        else:
            break

    # ✅ FINAL END CARD
    timeline.append({
        "type": "image",
        "file": "assets/images/journey-end-card.png",
        "duration": 4.0
    })

    return timeline