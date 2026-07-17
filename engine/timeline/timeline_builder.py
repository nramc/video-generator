import json
import os


def load_timeline(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Timeline file not found: {path}")

    with open(path, "r") as f:
        timeline = json.load(f)
    
    validate_timeline(timeline)
    return timeline


def validate_timeline(timeline):
    for item in timeline:
        if "file" not in item:
            raise ValueError("Each timeline item must have 'file'")

        if not os.path.exists(item["file"]):
            raise FileNotFoundError(f"Missing file: {item['file']}")
     
def get_intro_media(media_files):
    if not media_files:
        return None, []

    first = media_files[0]
    rest = media_files[1:]

    return first, rest

def create_intro_entry(file, duration=5.0):
    if file.lower().endswith((".mp4", ".mov", ".mkv")):
        return {
            "type": "video",
            "file": file,
            "start": 0,
            "end": duration
        }
    else:
        return {
            "type": "image",
            "file": file,
            "duration": duration
        }