from beat_detector import detect_beats


def group_beats(beat_times, step=4):
    return [beat_times[i] for i in range(0, len(beat_times), step)]


def beats_to_durations(beat_times):
    return [
        float(beat_times[i+1] - beat_times[i])
        for i in range(len(beat_times) - 1)
    ]

def generate_duration_using_beats(music_path):
    beats = detect_beats(music_path)

    grouped = group_beats(beats, step=4)
    durations = beats_to_durations(grouped)

    return durations

def generate_timeline_using_beats(media_files, music_path):
    durations = generate_duration_using_beats(music_path)

    timeline = build_timeline(media_files, durations)

    return timeline


def build_timeline(media_files, durations):
    timeline = []

    for i, duration in enumerate(durations):
        file = media_files[i % len(media_files)]

        duration = max(2.0, duration)   # ✅ avoid too short clips

        if file.endswith(".jpg"):
            timeline.append({
                "type": "image",
                "file": file,
                "duration": duration
            })
        else:
            timeline.append({
                "type": "video",
                "file": file,
                "start": 0,
                "end": duration
            })

    return timeline