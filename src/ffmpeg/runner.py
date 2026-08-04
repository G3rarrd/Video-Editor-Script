import subprocess
from .progress import timestamp_progress_bar


def run_ffmpeg(cmd: list[str], duration: int | None = None):
    process = subprocess.Popen(
        cmd,
        stderr=subprocess.PIPE,
        universal_newlines=True,
    )

    if duration is None:
        process.wait()
    else:
        timestamp_progress_bar(duration, process)

    return process.returncode