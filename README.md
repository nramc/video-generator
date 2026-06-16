

### Installation

1. Setup Virtual Environment
   ```bash
   python3 -m venv dev 
   ```
2. Install required dependencies
   ```bash
      source dev/bin/activate
      pip install -r requirements.txt
      export DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib
   ```
3. Run Application
    ```bash
      python cli.py --timeline timeline.json --music assets/musics/music.mp3

      python cli.py --auto-beat --music assets/musics/music.mp3 --media assets
    ```