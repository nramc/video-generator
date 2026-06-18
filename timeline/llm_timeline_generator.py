import os
import subprocess
import json

from timeline.beat_detector import generate_duration_using_beats
from utils.date_utils import get_file_name_with_date


def generate_timeline_using_llm(media_files, music_file):
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    files_str = "\n".join(media_files)
    durations = generate_duration_using_beats(music_file)

    prompt = f"""
You are a video editor AI.

Goal:
Create a clean video timeline JSON that combines the following media files (images and videos) with the provided background music.
The timeline should be engaging and well-paced, matching the rhythm and mood of the music. Duration each file based on duration extracted from the music beats.


Rules:
- DO NOT skip any file
- Use all files at least once
- Keep order meaningful
- Assign importance (1 = normal, 2 = important highlight) and duration for each file based on the music and importance
- Arrange files in a way that creates a compelling narrative or visual flow, while adhering to the rhythm and mood of the music.
- Assign duration (in seconds) for each file (for both images and videos) based on the music and importance from the beats. Combine shorter beats to create longer durations for important highlights.
- Only output **valid** JSON array, no explanations, no extra text, no comments.

Media files:
{files_str}

Background music file:
{music_file}

Music beat durations (in seconds):
{durations}

Output format:
[
  {{
    "file": "...",
    "type": "image or video",
    "importance": 1, # 1 = normal, 2 = important highlight
    "duration": 3.0,  # for both images and videos
    "start": 4.0,     # where to start in the video (for videos, this is the start position in the video)
    "end": 7.0        # where to end in the video (for videos, this is the end position in the video)
  }}
]
"""

    result = subprocess.run(
        ["ollama", "run", "llama3", prompt],
        capture_output=True,
        text=True
    )

    raw = result.stdout

    # extract JSON
    start = raw.find("[");
    json_text = raw[start:]

    timeline = json.loads(json_text)


    output_path = os.path.join(output_dir, get_file_name_with_date("timeline_llm.json"))
    with open(output_path, "w") as f:
      json.dump(timeline, f, indent=2)

    print(f"✅ LLM timeline saved: {output_path}")

    return timeline
