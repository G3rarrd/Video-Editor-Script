from pathlib import Path
from utils.validation import (file_exists, 
                              is_video_file, 
                              is_valid_timestamp_format, 
                              is_timestamp_within_video,
                              is_valid_cut_range,
                              is_valid_speed
                              )

def get_existing_file(prompt: str) -> Path:
    while True:
        input_vid : Path = Path(input(prompt).strip().replace('"', ''))

        if not file_exists(input_vid):
            print("Error: File does not exist.")
            continue
        
        if not is_video_file(input_vid):
            print("Error: File must be a video file")
            continue
        
        return input_vid


def get_cut_range(video_duration: float) -> tuple[str, str]:
    while True:
        start_time = get_timestamp(
            "Enter start timestamp (HH:MM:SS): ", 
            video_duration
        )
        
        end_time = get_timestamp(
            "Enter end timestamp (HH:MM:SS): ", 
            video_duration
        )
        
        if is_valid_cut_range(start_time, end_time):
            return start_time, end_time
        
        print("End time must be greater than start time.")


def get_timestamp(prompt: str, duration : float) -> str:
    while True:
        timestamp = input(prompt).strip()
        
        if not is_valid_timestamp_format(timestamp):
            print("Invalid timestamp format.")
            continue
        
        if not is_timestamp_within_video(timestamp, duration):
            print("Timestamp is outside the video.")
            continue
        
        return timestamp


def get_yes_no(prompt: str) -> bool:
    while True:
        choice = input(prompt).strip().lower()

        if choice in ("y", "yes"):
            return True

        if choice in ("n", "no"):
            return False

        print("Please enter y or n.")

        
def get_speed_multiplier(prompt: str) -> float:
    while True:
        try:
            speed :float = float(input(prompt))
            
            if not is_valid_speed(speed):
                print("Speed must be greater than zero.")
                continue
            
            return speed
        
        except ValueError:
            print("Please enter a valid number.")