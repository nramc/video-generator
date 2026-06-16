from timeline.beat_detector import beats_to_durations, detect_beats, group_beats

beats = detect_beats("assets/musics/music.mp3")

grouped = group_beats(beats, step=4)

durations = beats_to_durations(grouped)

print(durations[:5])

