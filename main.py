import subprocess
from moviepy import *
import numpy as np
import json
import io
import tempfile
import os
import pysrt

with open("config.json") as json_file:
    config = json.load(json_file)

print("config")
print(config)

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

subtitle_clips = []
for sub in subtitles:
    start_time = sub.start.ordinal / 1000  # Convert to seconds
    end_time = sub.end.ordinal / 1000
    duration = end_time - start_time


    text_clip = (
        TextClip(
            "./fonts/tiktoksans/TikTokDisplay-Bold.ttf", 
            text="Тест субтитров 🔟 ⺻ 𑆏", 
            size=(600, None),
            font_size=100,
            color="white",
            method='caption',
            stroke_color='black',
            stroke_width=1,
            bg_color=None,  
            transparent=True,
            text_align='center', 
            interline=4 
        )
        .with_position(('center', 'bottom'))
        .with_duration(2)
        .with_start(0))

    
    subtitle_clips.append(text_clip)



# Video
videoFileClip = VideoFileClip(f'./video/{config["videoSource"]}')

content_clip = videoFileClip.subclipped(
    config["startTime"], config["endTime"]
)

# Get the dimensions of the original video
video_width, video_height = content_clip.size

# Calculate dimensions for TikTok format (9:16)
target_width = 1080  # Standard TikTok width
target_height = 1920  # Standard TikTok height

# Always scale based on width to preserve full width of the video
new_width = target_width
new_height = int(video_height * (target_width / video_width))
resized_clip = content_clip.resized(width=target_width)

# Create a blurred background from the content clip
background = (
    content_clip
    .resized(width=target_width * 1.2)  # Make it slightly larger to fill any gaps
    # .fx(blur, sigma=10)  # Add gaussian blur effect
    .with_duration(content_clip.duration)
)

# Center the background clip
x_bg = -(background.size[0] - target_width) // 2  # Center horizontally
y_bg = -(background.size[1] - target_height) // 2  # Center vertically

# Center the video vertically on the background
x_center = 0  # No horizontal offset needed since we're using full width
y_center = (target_height - resized_clip.size[1]) // 2




final_clip = CompositeVideoClip(
    [
        background.with_position((x_bg, y_bg)),  # Position the blurred background
        resized_clip.with_position((x_center, y_center))
    ] + subtitle_clips,
    size=(target_width, target_height)  # Ensure the final size is correct
)

# Set the audio of the video clip to the new audio clip
final_clip = final_clip.with_audio(audio_clip)  # Changed from set_audio to with_audio
final_clip.write_videofile("./result/result.mp4")

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
