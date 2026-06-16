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

def generate_duration_using_beats(music_path):
    beats = detect_beats(music_path)

    grouped = group_beats(beats, step=4)
    durations = beats_to_durations(grouped)

    return durations