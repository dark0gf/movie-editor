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

# Video
videoFileClip = VideoFileClip(f'./video/{config["videoSource"]}')

clip1 = videoFileClip.subclipped(
    config["startTime"], config["endTime"]
)

# Subtitles add to vide
subtitles = pysrt.open(temp_subtitle_file)

subtitle_clips = []
for sub in subtitles:
    start_time = sub.start.ordinal / 1000  # Convert to seconds
    end_time = sub.end.ordinal / 1000
    duration = end_time - start_time
    
    # text_clip = TextClip(
    #     sub.text,
    #     font='Arial',
    #     size=(clip1.w, None),
    #     method='caption',
    #     color='white',
    #     stroke_color='black',
    #     stroke_width=2,
    #     font_size=24
    # ).set_position(('center', 'bottom')).set_duration(duration).set_start(start_time)

    text_clip = (
        TextClip(sub.text, fontsize=30, color="white", font="Arial")
        .set_position(("center", "top"))
        .set_duration(video.duration)
    )

    
    subtitle_clips.append(text_clip)

final_clip = CompositeVideoClip(
    [
        clip1,
    ] + subtitle_clips
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
