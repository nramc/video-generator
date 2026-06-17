

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
      python cli.py --timeline timeline.json --music assets/musics/music.mp3 --title='My First Automated Journey' --subtitle='Native Place: 19.01.2025'

      python cli.py --auto-beat --music assets/musics/music.mp3 --media assets --title='My First Automated Journey' --subtitle='Native Place: 19.01.2025'

      python cli.py --auto-beat --media assets/ --music assets/musics/music.mp3 --use-llm --title='My First Automated Journey' --subtitle='Native Place: 19.01.2025'
    ```