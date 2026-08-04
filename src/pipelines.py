from pathlib import Path

from ffmpeg.cut_video import cut_video
from ffmpeg.gif import video_to_gif
from ffmpeg.metadata import get_video_duration

from ffmpeg.speed import speed_up_video
from models.video import VideoContext

from cli.prompts import (
    get_cut_range,
    get_speed_multiplier,
    get_yes_no,
)

from utils.paths import (
    unique_output_path
)

def cut_video_pipeline(video : VideoContext):
    # Define your paths
    input_vid = video.path
    
    input_name = input_vid.stem
    input_ext = input_vid.suffix

    start_time, end_time = get_cut_range(video.duration)
    
    remove_audio : bool= get_yes_no("Remove audio? (y/n): ")
    
    output_name : str = input("Enter output edit name (optional): ")
    
    output_name_path = Path(f"{output_name}{input_ext}" if output_name != "" else 
        f"{input_name}{'_no_audio' if remove_audio else ''}_edit{input_ext}"
    )
    
    output = unique_output_path(
        input_vid.parent,
        output_name_path,
        
    )

    cut_video(
        input_file=input_vid, 
        output_file_name=output, 
        start_time=start_time, 
        end_time=end_time,
        remove_audio=remove_audio
    )
    
    print(f"Video cut saved: {output}")

def video_to_gif_pipeline(video : VideoContext):
    input_vid = video.path
    input_name = input_vid.stem

    fps = int(input("Enter FPS: "))
    resolution = int(input("Enter Resolution: "))
    output_name: str = input("Enter output edit name (optional): ")
    output_name_path = Path(f"{input_name}.gif" if output_name == "" else f"{output_name}.gif")
    
    output = unique_output_path(
        input_vid.parent,
        output_name_path,
    )

    video_to_gif(
        input_file=input_vid, 
        output_file_name=output, 
        resolution=resolution, 
        fps=fps,
        duration=int(video.duration)
    )
    
    print(f"gif saved: {output}")

def speed_up_video_pipeline(video : VideoContext):
    input_vid = video.path
    
    input_name = input_vid.stem
    input_ext = input_vid.suffix
    
    speed = get_speed_multiplier("Speed multiplier (e.g. 2, 1.5, 0.5): ")
    
    output_name: str = input("Enter output edit name (optional): ")
    
    output_name_path = Path(f"{input_name}{input_ext}" if output_name == "" else f"{output_name}{input_ext}")
    
    output = unique_output_path(input_vid.parent, output_name_path)
    
    speed_up_video(
        input_file=input_vid,
        output_file_name=output,
        speed=speed,
        duration=int(video.duration)
    )
    
    print(f"Sped video saved: {output}")