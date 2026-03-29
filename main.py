import re
import ffmpeg
import subprocess
from tqdm import tqdm
from pathlib import Path

def timestamp_to_seconds(timestamp : str):
    h, m, s = map(int, timestamp.split(":"))
    return h * 3600 + m * 60 + s

def process_video(cmd, duration:int):
    """ Video Processing Stage """

    # Opens FFmpeg as a subprocess
    process = subprocess.Popen(
        cmd, stderr=subprocess.PIPE, universal_newlines=True
    )
    timestamp_progress_bar(duration, process)
    return process.returncode

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

def is_valid_timestamp(timestamp : str):
    # Regex to check HH:MM:SS format
    return bool(re.match(r'^(?:[01]?\d|2[0-3]):[0-5]\d:[0-5]\d$', timestamp))


def video_to_gif(input_file: Path, output_file_name: Path, resolution: int, fps: int):
    target_dir = input_file.parent
    base_stem = output_file_name.stem
    output_file = target_dir / f"{base_stem}.gif"

    counter = 1
    while output_file.exists():
        output_file =target_dir / f"{base_stem}_{counter}.gif"
        counter += 1

    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-vf", f"fps={fps}, scale={resolution}:-1:flags=lanczos,split[s0][s1];[s0]palettegen=max_colors=128:stats_mode=diff[p];[s1][p]paletteuse=dither=bayer:bayer_scale=5:diff_mode=rectangle",
        output_file
    ]

    subprocess.run(cmd)


def cut_video(input_file: Path, output_file_name: Path, start_time: str, end_time: str, remove_audio:bool):
    """ Video Cut Settings """
    target_dir = input_file.parent
    base_stem = output_file_name.stem
    ext = output_file_name.suffix
    output_file = target_dir / output_file_name

    counter = 1
    while output_file.exists():
        output_file = target_dir / f"{base_stem}_{counter}{ext}"
        counter += 1

    duration = timestamp_to_seconds(end_time) - timestamp_to_seconds(start_time)

    cmd = [
        "ffmpeg",
        "-i", str(input_file),
        "-ss", start_time,
        "-to", end_time,
        "-c:v", "libx264",    # re-encode for eaxct frame
        "-crf", "18",         # high quality
    ]

    if remove_audio:
        cmd.append("-an") # no audio

    else:
        cmd.extend(["-c:a", "aac"]) # encode audio
        cmd.extend(["-b:a", "256k"]) # audio bitrate

    cmd.append(str(output_file))

    try:
        returncode = process_video(cmd, duration)
        if returncode == 0:
            print(f"Success: {output_file}")
        else:
            print(f"FFmpeg failed with return code {returncode}")

    except ffmpeg.Error as e:
        err_msg = e.stderr.decode() if e.stderr else "Unknown FFmpeg error"
        print(f"Error occurred: {err_msg}")


def video_to_gif_pipeline():
    get_input_path = input("Enter Video Path: ").strip()
    input_vid = Path(get_input_path)
    input_name = input_vid.stem

    if not input_vid.exists() or not input_vid.is_file():
        print(f"Error: The file '{input_vid}' does not exist.")

    else:
        fps = int(input("Enter FPS: "))
        resolution = int(input("Enter Resolution: "))
        output_name = Path(f"{input_name}.gif")

        video_to_gif(
            input_file=input_vid, 
            output_file_name=output_name, 
            resolution=resolution, 
            fps=fps
            )

    
def cut_video_pipeline():
    # Define your paths
    get_input_path = input("Enter Video Path: ").strip()
    input_vid = Path(get_input_path)
    input_name = input_vid.stem
    input_ext = input_vid.suffix

    if not input_vid.exists() or not input_vid.is_file():
        print(f"Error: The file '{input_vid}' does not exist.")

    else:
        # 2. Validate Timestamps
        start_time = input("Enter start timestamp (HH:MM:SS): ").strip()
        end_time = input("Enter end timestamp (HH:MM:SS): ").strip()

        if not is_valid_timestamp(start_time) or not is_valid_timestamp(end_time):
            print("Error: Timestamps must be in HH:MM:SS format.")

        elif timestamp_to_seconds(start_time) >= timestamp_to_seconds(end_time):
            print("Error: Start time must be earlier than end time.")

        else:
            choice = input("Remove audio? (y/n): ").strip().lower()
            remove_audio : bool = choice.startswith("y")

            # 3. Define Output name as a path
            output_name = Path(f"{input_name}_{"no_audio_" if remove_audio else ""}edit.{input_ext}")
            
            cut_video(
                input_file=input_vid, 
                output_file_name=output_name, 
                start_time=start_time, 
                end_time=end_time,
                remove_audio=remove_audio
            )

if __name__ == "__main__":
    cut_video_pipeline()



