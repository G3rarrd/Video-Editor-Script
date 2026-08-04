from pathlib import Path

from .runner import run_ffmpeg
from utils.paths import unique_output_path
from utils.time import timestamp_to_seconds


def cut_video(
    input_file: Path,
    output_file_name: Path,
    start_time: float,
    end_time: float,
    remove_audio: bool,
):
    output = unique_output_path(
        input_file.parent,
        output_file_name,
    )

    duration = (
        timestamp_to_seconds(end_time)
        - timestamp_to_seconds(start_time)
    )

    cmd = [
        "ffmpeg",
        "-i",
        str(input_file),
        "-ss",
        start_time,
        "-to",
        end_time,
        "-c:v",
        "libx264",
        "-crf",
        "18",
    ]

    if remove_audio:
        cmd.append("-an")
    else:
        cmd.extend(["-c:a", "aac"])
        cmd.extend(["-b:a", "256k"])

    cmd.append(str(output))

    return run_ffmpeg(cmd, duration)