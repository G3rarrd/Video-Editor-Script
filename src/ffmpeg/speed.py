from pathlib import Path

from ffmpeg.runner import run_ffmpeg
from utils.paths import unique_output_path

def speed_up_video(
    input_file: Path,
    output_file_name: Path,
    speed: float,
    duration : float
):
    
    output = unique_output_path(
        input_file.parent,
        output_file_name,
    )
    
    cmd = build_speed_command(input_file, output_file=output, speed=speed)
    
    return run_ffmpeg(cmd, int(duration / speed)) 
        
def get_audio_filter(speed : float) -> str:
    # Audio speed
    if 0.5 <= speed <= 2.0:
        return f"atempo={speed}"
    else:
        # Chain atempo filters
        filters = []
        remaining = speed

        while remaining > 2:
            filters.append("atempo=2.0")
            remaining /= 2

        while remaining < 0.5:
            filters.append("atempo=0.5")
            remaining /= 0.5

        filters.append(f"atempo={remaining}")

        return ",".join(filters)
    
def build_speed_command(
    input_file: Path,
    output_file: Path,
    speed: float,
) -> list[str]:
    return [
        "ffmpeg",
        "-i", str(input_file),
        "-filter:v", f"setpts={1 / speed}*PTS",
        "-filter:a", get_audio_filter(speed),
        "-c:v", "libx264",
        "-c:a", "aac",
        str(output_file),
    ]