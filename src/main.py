from cli.prompts import get_existing_file
from pathlib import Path
from ffmpeg.metadata import get_video_duration
from models.menu import display_menu, execute_choice
from models.video import VideoContext
from utils.time import seconds_to_timestamp


def main():
    while True:
        # Video Information
        video_path : Path = get_existing_file("Enter Video Path: ")
        duration : float = get_video_duration(video_path)
        
        video = VideoContext(
            path=video_path,
            duration=duration
            )
        
        video_time : str = seconds_to_timestamp(duration)
        print(f"\nTitle: {video_path.stem}{video_path.suffix}\n"
                f"Duration: {video_time}\n")
        
        display_menu()
        
        choice = input("Choose an option: ").strip()
        
        if not execute_choice(choice, video):
            break
        
        print("")


if __name__ == "__main__":
    main()