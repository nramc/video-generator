import argparse

from renderer.renderer import render_video
from timeline.beats_timeline_generator import generate_timeline_using_beats
from timeline.llm_timeline_generator import generate_timeline_using_llm
from timeline.timeline_builder import load_timeline
from utils.date_utils import get_file_name_with_date
from utils.media_loader import load_media_files


def main():
    parser = argparse.ArgumentParser(description="Local Video Generator CLI")

    parser.add_argument("--music", required=True, help="Path to music file")
    parser.add_argument("--media",help="Path to folder containing images/videos",required=False)

    
    parser.add_argument("--output", default="output/"+get_file_name_with_date("output.mp4"), help="Path to output video")

    parser.add_argument("--timeline", help="Path to timeline.json")
    parser.add_argument("--use-llm", action="store_true", help="Generate timeline via LLM")
    parser.add_argument("--auto-beat", action="store_true", help="Generate timeline via auto beat detection")

    args = parser.parse_args()

    timeline = None
    
    if args.timeline:
        timeline_path = args.timeline
        timeline = load_timeline(timeline_path)
    elif args.auto_beat:
        if not args.media:
            raise ValueError("❌ Please provide --media folder")
        
        media_files = load_media_files(args.media)
        print(f"✅ Found {len(media_files)} media files")

        if args.use_llm:
            timeline = generate_timeline_using_llm(media_files, args.music)
        else:
            timeline = generate_timeline_using_beats(media_files, args.music)

    if timeline is None:
        raise ValueError("❌ No timeline provided. Use --timeline, --use-llm or --auto-beat")
    
    render_video(timeline, args.music, args.output)

if __name__ == "__main__":
    main()