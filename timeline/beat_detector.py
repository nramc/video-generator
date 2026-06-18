import librosa
import numpy as np


def detect_beats(audio_file):
    print("🔍 Detecting beats...")

    y, sr = librosa.load(audio_file)

    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)

    tempo_value = float(tempo) if not isinstance(tempo, np.ndarray) else float(tempo[0])

    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    print(f"✅ Tempo: {tempo_value:.2f} BPM")
    print(f"✅ Found {len(beat_times)} beats")

    return beat_times


def group_beats(beat_times, step=4):
    return [beat_times[i] for i in range(0, len(beat_times), step)]


def beats_to_durations(beat_times):
    return [
        float(beat_times[i+1] - beat_times[i])
        for i in range(len(beat_times) - 1)
    ]

def enforce_min_duration(beat_times, min_duration=3.0):
    filtered = [beat_times[0]]
    acc_time = 0.0

    for i in range(1, len(beat_times)):
        delta = beat_times[i] - beat_times[i - 1]
        acc_time += delta

        if acc_time >= min_duration:
            filtered.append(beat_times[i])
            acc_time = 0.0

    return filtered

def generate_duration_using_beats(music_path):
    beats = detect_beats(music_path)

    grouped = group_beats(beats, step=4)
    print(f"✅ Grouped beats: {len(grouped)}")


    # Enforce minimum duration
    filtered = enforce_min_duration(grouped, min_duration=3.0)
    print(f"✅ Grouped beats (min duration 3s): {len(filtered)}")


    durations = beats_to_durations(filtered)
    print(f"✅ Generated durations: {len(durations)}")

    return durations