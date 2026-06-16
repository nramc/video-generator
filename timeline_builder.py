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
        

def apply_beat_durations(llm_timeline, durations):
    timeline = []

    for i, item in enumerate(llm_timeline):
        duration = durations[i % len(durations)]

        duration = max(2.0, duration)

        if item["type"] == "image":
            timeline.append({
                "type": "image",
                "file": item["file"],
                "duration": duration
            })

        else:
            timeline.append({
                "type": "video",
                "file": item["file"],
                "start": item.get("start", 0),
                "end": item.get("start", 0) + duration
            })

    return timeline
