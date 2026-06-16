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
