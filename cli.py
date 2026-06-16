import argparse
from renderer import render_video
from timeline_builder import load_timeline
from llm_generator import generate_timeline_if_needed

def main():
    parser = argparse.ArgumentParser(description="Local Video Generator CLI")

    parser.add_argument("--timeline", help="Path to timeline.json")
    parser.add_argument("--music", required=True)
    parser.add_argument("--output", default="output/output.mp4")

    parser.add_argument("--use-llm", action="store_true", help="Generate timeline via LLM")

    args = parser.parse_args()

    if args.use_llm:
        timeline_path = generate_timeline_if_needed()
    else:
        timeline_path = args.timeline

    timeline = load_timeline(timeline_path)

    render_video(timeline, args.music, args.output)

if __name__ == "__main__":
    main()