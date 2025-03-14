from moviepy import *
import numpy as np
import json

with open("config.json") as json_file:
    config = json.load(json_file)

print(config)

videoFileClip = VideoFileClip(config.videoSource)

clip1 = videoFileClip.subclipped(
    "00:03:34.75", "00:03:56.80"
)







final_clip = CompositeVideoClip(
    [
        clip1,
    ]
)
final_clip.write_videofile("./video/result.mp4")

from moviepy.editor import AudioFileClip
import subprocess

# Get audio stream using ffmpeg (without saving it to a temp file)
command = 'ffmpeg -i ./video/Scott.Pilgrim.vs.the.World.2010.BDRip.1080p.Rus.Eng.mkv -map 0:a:1 -f nut -'
process = subprocess.run(command, capture_output=True, text=True, shell=True)

# Convert audio stream to bytes
audio_stream = process.stdout.encode('utf-8')

# Create an audio clip from the bytes
audio_clip = AudioFileClip(audio_stream)

# Set the audio of the video clip to the new audio clip
final_clip = final_clip.set_audio(audio_clip)

# Write the final video file
final_clip.write_videofile("./video/result.mp4")
