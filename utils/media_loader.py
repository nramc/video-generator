import os

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".mp4", ".mov", ".mkv")


def load_media_files(folder):
    media_files = []

    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(SUPPORTED_EXTENSIONS):
                full_path = os.path.join(root, file)
                media_files.append(full_path)

    media_files.sort()  # ✅ deterministic order
    return media_files