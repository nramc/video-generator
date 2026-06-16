import subprocess
import json

OUTPUT_FILE = "timeline.json"


def generate_timeline_if_needed():
    prompt = """
Create a JSON video timeline.

Assets:
- images: assets/images/img1.jpg, img2.jpg
- video: assets/videos/clip1.mp4

Output JSON format:
[
  {"type": "image", "file": "...", "duration": 3},
  {"type": "video", "file": "...", "start": 0, "end": 5}
]

ONLY output valid JSON.
"""

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )

    output = result.stdout

    # crude extraction (can improve later)
    json_start = output.find("[")
    json_data = output[json_start:]

    with open(OUTPUT_FILE, "w") as f:
        f.write(json_data)

    return OUTPUT_FILE