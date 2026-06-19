from concurrent.futures import ThreadPoolExecutor
import json

from moviepy import VideoFileClip
import random

from timeline.beat_detector import generate_duration_using_beats
from timeline.timeline_builder import create_intro_entry, get_intro_media
from utils.date_utils import get_file_name_with_date
from utils.video_normalizer import ensure_valid_video



def generate_timeline_using_beats(media_files, music_path):
    durations = generate_duration_using_beats(music_path)

    intro_media, remaining_media = get_intro_media(media_files)

    timeline = build_timeline(remaining_media, durations[1:])


    if intro_media:
        intro_entry = create_intro_entry(intro_media, duration=durations[0])
        timeline.insert(0, intro_entry)

    save_timeline(timeline)
    return timeline


def save_timeline(timeline, output_path=None):
    if output_path is None:
        output_path= "output/"+ get_file_name_with_date("timeline_beat.json")

    with open(output_path, "w") as f:
        json.dump(timeline, f, indent=2)

    print(f"✅ Timeline saved to {output_path}")

def build_timeline(media_files, durations, max_video_reuse=3):
    timeline = []

    images, video_files = split_media_files(media_files)
    videos = load_videos(video_files)
    video_info = prepare_video_info(videos)

    random.shuffle(images)

    state = init_state()

    for duration in durations:
        duration = float(max(2.0, duration))

        use_video = should_use_video(duration, videos)

        # ✅ IMAGE
        if not use_video:
            entry = get_next_image(images, state, duration)
            if entry:
                timeline.append(entry)
                continue

        # ✅ VIDEO
        entry = process_video_clip(
            duration,
            videos,
            video_info,
            state,
            max_video_reuse
        )

        if entry:
            timeline.append(entry)
        else:
            break

    return timeline

def split_media_files(media_files):
    image_ext = (".jpg", ".jpeg", ".png")
    video_ext = (".mp4", ".mov", ".mkv")

    images = [f for f in media_files if f.lower().endswith(image_ext)]
    videos = [f for f in media_files if f.lower().endswith(video_ext)]

    for f in media_files:
        if not f.lower().endswith(image_ext) and not f.lower().endswith(video_ext):
            print(f"⚠️ Unsupported media file (ignored): {f}")

    return images, videos

from concurrent.futures import ThreadPoolExecutor

def load_videos(video_files):
    with ThreadPoolExecutor(max_workers=4) as executor:
        return list(executor.map(ensure_valid_video, video_files))
    
from moviepy import VideoFileClip

def prepare_video_info(videos):
    info = {}

    for f in videos:
        clip = VideoFileClip(f)
        info[f] = {
            "clip": clip,
            "duration": clip.duration
        }

    return info

def init_state():
    return {
        "image_index": 0,
        "last_video_file": None,
        "video_usage": {},
        "video_count": {},
        "video_segments_used": {}
    }

def should_use_video(duration, videos):
    if not videos:
        return False

    # probability increases with duration
    prob = min(1.0, max(0.2, duration / 5.0))

    return random.random() < prob

def get_next_image(images, state, duration):
    if state["image_index"] >= len(images):
        return None

    file = images[state["image_index"]]
    state["image_index"] += 1

    return {
        "type": "image",
        "file": file,
        "duration": duration
    }

def process_video_clip(duration, videos, video_info, state, max_video_reuse):
    pool = build_weighted_pool(videos, video_info, state, max_video_reuse)

    if not pool:
        return None

    file = select_video_file(pool)

    start, end = select_video_segment(file, duration, video_info, state)

    update_video_state(file, duration, start, end, state)

    return create_video_entry(file, start, end)

def build_weighted_pool(videos, video_info, state, max_video_reuse):
    pool = []

    for f in videos:
        if f == state["last_video_file"]:
            continue

        if state["video_count"].get(f, 0) >= max_video_reuse:
            continue

        info = video_info[f]
        remaining = info["duration"] - state["video_usage"].get(f, 0)

        if remaining <= 0:
            continue

        weight = remaining

        if state["video_count"].get(f, 0) == 0:
            weight *= 2

        pool.append((f, weight))

    return pool

def select_video_file(pool):
    files = [f for f, _ in pool]
    weights = [w for _, w in pool]

    return random.choices(files, weights=weights, k=1)[0]

def select_video_segment(file, duration, video_info, state):
    clip = video_info[file]["clip"]
    video_length = video_info[file]["duration"]

    max_start = max(0, video_length - duration)

    used_segments = state["video_segments_used"].get(file, [])

    best_start = 0
    best_score = -1

    for _ in range(6):
        candidate = random.uniform(0, max_start) if max_start > 0 else 0

        if not used_segments:
            return candidate, candidate + duration

        min_dist = min(
            min(abs(candidate - start), abs(candidate - end))
            for start, end in used_segments
        )

        if min_dist > best_score:
            best_score = min_dist
            best_start = candidate

    return best_start, best_start + duration

def update_video_state(file, duration, start, end, state):
    state["last_video_file"] = file

    state["video_usage"][file] = state["video_usage"].get(file, 0) + duration
    state["video_count"][file] = state["video_count"].get(file, 0) + 1

    state["video_segments_used"].setdefault(file, []).append((start, end))

def create_video_entry(file, start, end):
    return {
        "type": "video",
        "file": file,
        "start": start,
        "end": end
    }
