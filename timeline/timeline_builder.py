import json
import os


def load_timeline(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Timeline file not found: {path}")

    with open(path, "r") as f:
        timeline = json.load(f)

    # ✅ FINAL END CARD
    timeline.append({
        "type": "image",
        "file": "assets/images/journey-end-card.png",
        "duration": 4.0
    })
    validate_timeline(timeline)
    return timeline


def validate_timeline(timeline):
    for item in timeline:
        if "file" not in item:
            raise ValueError("Each timeline item must have 'file'")

        if not os.path.exists(item["file"]):
            raise FileNotFoundError(f"Missing file: {item['file']}")
     