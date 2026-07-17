import subprocess
import os


def is_video_valid(path: str) -> bool:
    # Check first-frame decode (matches MoviePy failure)
    first_frame = subprocess.run(
        [
            "ffmpeg", "-v", "error",
            "-i", path,
            "-frames:v", "1",
            "-f", "image2", "-"
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
    )

    if first_frame.returncode != 0:
        return False

    # Full decode check
    full_check = subprocess.run(
        [
            "ffmpeg",
            "-v", "error",
            "-err_detect", "explode",
            "-i", path,
            "-f", "null",
            "-"
        ],
        stderr=subprocess.PIPE,
        stdout=subprocess.DEVNULL,
    )

    return full_check.returncode == 0


def reencode_video(input_path: str) -> str:
    output_path = input_path.replace(".mp4", "_fixed.mp4")

    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "aac",
        output_path
    ], check=True)

    # os.remove(input_path)

    return output_path


def ensure_valid_video(path: str) -> str:
    if is_video_valid(path):
        return path

    print(f"[CI] Fixing broken/incompatible video: {path}")
    return reencode_video(path)
