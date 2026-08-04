import re
from tqdm import tqdm
import subprocess

def timestamp_progress_bar(duration: int, process: subprocess.Popen[str]):
    # Regex to match time in ffmpeg output
    time_pattern = re.compile(r'time=(\d+):(\d+):(\d+)')

    # initialize tqdm progress bar
    p_bar = tqdm(total=duration, unit="sec", desc="Processing", dynamic_ncols=True)

    # Loading bar
    for line in process.stderr:
        line = line.strip()
        match = time_pattern.search(line) # find time pattern on the process.stderr line
        if match:
            h, m, s = map(int, match.groups())
            elapsed = h*3600 + m*60 + s

            p_bar.n = min(elapsed, duration)
            p_bar.refresh()

    # max out bar
    p_bar.n = duration
    p_bar.refresh()

    # end
    process.wait()
    p_bar.close()