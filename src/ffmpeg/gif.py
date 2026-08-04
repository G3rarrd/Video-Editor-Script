from pathlib import Path

from ffmpeg.runner import run_ffmpeg
from utils.paths import unique_output_path


def video_to_gif(
    input_file: Path,
    output_file_name: Path,
    resolution: int,
    fps: int,
    duration : float,
):
    output = unique_output_path(
        input_file.parent,
        output_file_name,
    )

    cmd = [
        "ffmpeg",
        "-i",
        str(input_file),
        "-vf",
        f"fps={fps},scale={resolution}:-1:flags=lanczos,"
        "split[s0][s1];"
        "[s0]palettegen=max_colors=128:stats_mode=diff[p];"
        "[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        str(output),
    ]

    run_ffmpeg(cmd, int(duration))