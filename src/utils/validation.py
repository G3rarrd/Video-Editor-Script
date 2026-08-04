from .time import timestamp_to_seconds
import re
from pathlib import Path

def validate_timestamps(start_time : str, end_time : str):
    while True:
        if timestamp_to_seconds(start_time) >= timestamp_to_seconds(end_time):
            print("Start time must be earlier than end time.")
            continue
        break

def is_timestamp_within_video(
    timestamp: str,
    video_duration: float,
) -> bool:
    """Check that a timestamp falls within the video's duration."""
    return 0 <= timestamp_to_seconds(timestamp) <= video_duration
    
def is_valid_timestamp_format(timestamp : str):
    # Regex to check HH:MM:SS format
    return bool(re.match(r'^(?:[01]?\d|2[0-3]):[0-5]\d:[0-5]\d$', timestamp))

def is_valid_cut_range(start_time : str, end_time : str):
    return timestamp_to_seconds(end_time) > timestamp_to_seconds(start_time)

def file_exists(path: Path) -> bool:
    return path.exists() and path.is_file()

def is_video_file(path: Path) -> bool:
    return path.suffix.lower() in {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".flv",
    }

def is_valid_speed(speed: float) -> bool:
    return speed > 0