import subprocess
from moviepy import *
import numpy as np
import json
import io
import tempfile
import os
import pysrt
import cv2  # Import OpenCV for image processing

with open("config.json") as json_file:
    config = json.load(json_file)

print("config")
print(config)

# Calculate dimensions for TikTok format (9:16)
target_width = 1080  # Standard TikTok width
target_height = 1920  # Standard TikTok height

# Audio
temp_audio_file = './result/audio.wav'
command = [
    'ffmpeg',
    '-i', f'./video/{config["videoSource"]}',
    '-ss', config["startTime"],
    '-to', config["endTime"],
    '-map', f'0:a:{config["audioTrack"]}',
    '-acodec', 'pcm_s16le',
    '-y',
    temp_audio_file
]
process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
print(process.stderr.decode())
audio_clip = AudioFileClip(temp_audio_file)

# Subtitles extract
temp_subtitle_file = './result/subtitles.srt'
subtitle_command = [
    'ffmpeg',
    '-i', f'./video/{config["videoSource"]}',
    '-map', '0:s:0',
    '-c', 'copy',
    '-y',
    temp_subtitle_file
]
subprocess.run(subtitle_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Subtitles clips
subtitles = pysrt.open(temp_subtitle_file)


text_clip_height_offset = 600
subtitle_clips = []
for sub in subtitles:
    start_time = sub.start.ordinal / 1000  # Convert to seconds
    end_time = sub.end.ordinal / 1000
    duration = end_time - start_time


    text_clip_white = (
        TextClip(
            "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
            text="Text on english, Text on english, Text on english, Text on english",
            size=(target_width - 50, None),
            font_size=60,
            color="white",
            method='caption',
            stroke_color='black',
            stroke_width=1,
            bg_color=None,
            transparent=True,
            text_align='center',
            interline=6
        )
        .with_position(('center', 0))
        .with_start(0)
        .with_duration(2)
    )

    text_clip_white = (
        TextClip(
            "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
            text="Text on english, Text on english, Text on english, Text on english",
            size=(target_width - 50, text_clip_white.size[1] + 20),
            font_size=60,
            color="white",
            method='caption',
            stroke_color='black',
            stroke_width=1,
            bg_color=None,
            transparent=True,
            text_align='center',
            interline=6
        )
        .with_position(('center', text_clip_height_offset))
        .with_start(0)
        .with_duration(2)
    )

    print(f"text_clip_white dimensions: {text_clip_white.size}")

    text_clip_yellow = (
        TextClip(
            "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
            text="Texto en inglés, Texto en inglés, Texto en inglés, Texto en inglés",
            size=(target_width - 50, None),
            font_size=60,
            color="yellow",
            method='caption',
            stroke_color='black',
            stroke_width=1,
            bg_color=None,
            transparent=True,
            text_align='center',
            interline=4
        )
        .with_position(('center', text_clip_height_offset + text_clip_white.size[1]))
        .with_start(0)
        .with_duration(2)
    )

    text_clip_yellow = (
        TextClip(
            "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
            text="Texto en inglés, Texto en inglés, Texto en inglés, Texto en inglés",
            size=(target_width - 50, text_clip_yellow.size[1] + 20),
            font_size=60,
            color="yellow",
            method='caption',
            stroke_color='black',
            stroke_width=1,
            bg_color=None,
            transparent=True,
            text_align='center',
            interline=4
        )
        .with_position(('center', text_clip_height_offset + text_clip_white.size[1]))
        .with_start(0)
        .with_duration(2)
    )

    print(f"text_clip_yellow dimensions: {text_clip_yellow.size}")

    subtitle_clips.extend([text_clip_white, text_clip_yellow])


# Video
videoFileClip = VideoFileClip(f'./video/{config["videoSource"]}')

content_clip = videoFileClip.subclipped(
    config["startTime"], config["endTime"]
)

# Get the dimensions of the original video
video_width, video_height = content_clip.size

# Always scale based on width to preserve full width of the video
new_width = target_width
new_height = int(video_height * (target_width / video_width))
resized_clip = content_clip.resized(width=target_width*1.5)

# Define a custom blur function using OpenCV
def blur_frame(frame, sigma=10):
    # Apply Gaussian blur to the frame
    return cv2.GaussianBlur(frame, (sigma*2+1, sigma*2+1), sigma)

background = (
    content_clip
    .resized(width=target_width * 4)
    .with_duration(content_clip.duration)
    .transform(lambda get_frame, t: blur_frame(get_frame(t), sigma=30))
)

# Center the background clip
x_bg = -(background.size[0] - target_width) // 2  # Center horizontally
y_bg = -(background.size[1] - target_height) // 2  # Center vertically

x_center = -((resized_clip.size[0] - target_width) // 2)  # Center horizontally
y_center = (target_height - resized_clip.size[1]) // 2 - 300  # Center vertically


final_clip = CompositeVideoClip(
    [
        background.with_position((x_bg, y_bg)),  # Position the blurred background
        resized_clip.with_position((x_center, y_center))
    ] + subtitle_clips,
    size=(target_width, target_height)  # Ensure the final size is correct
)

# Set the audio of the video clip to the new audio clip
final_clip = final_clip.with_audio(audio_clip)  # Changed from set_audio to with_audio
result_file_path = "./result/result.mp4"
final_clip.write_videofile(result_file_path)

# Get information about the output file using ffmpeg
print("\n--- Output File Information ---")
ffmpeg_info_command = [
    'ffmpeg',
    '-i', result_file_path,
]
ffmpeg_info_process = subprocess.run(ffmpeg_info_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# FFmpeg outputs the file information to stderr
print(ffmpeg_info_process.stderr.decode())
print("--- End of Output File Information ---\n")

# Clean up resources
try:
    audio_clip.close()
except:
    pass

try:
    videoFileClip.close()
except:
    pass

try:
    final_clip.close()
except:
    pass

# Remove the temporary audio file
try:
    os.unlink(temp_audio_file)
except:
    pass

# Remove the temporary subtitle file
try:
    os.unlink(temp_subtitle_file)
except:
    pass

print("Video processing completed successfully!")
