import subprocess
from moviepy import *
import numpy as np
import json
import io
import tempfile
import os

with open("config.json") as json_file:
    config = json.load(json_file)

print("config")
print(config)

# Create a temporary file for the audio
temp_audio_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
temp_audio_file.close()

# Extract audio directly to the temporary file using ffmpeg
command = [
    'ffmpeg',
    '-i', f'./video/{config["videoSource"]}',
    '-ss', config["startTime"],  # Start time
    '-to', config["endTime"],    # End time
    '-map', '0:a:1',  # Select the second audio stream
    '-acodec', 'pcm_s16le',  # Use PCM format for better compatibility
    '-y',  # Overwrite output file if it exists
    temp_audio_file.name
]

# Run the command
process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# Create an AudioFileClip from the temporary file
audio_clip = AudioFileClip(temp_audio_file.name)

videoFileClip = VideoFileClip(f'./video/{config["videoSource"]}')

clip1 = videoFileClip.subclipped(
    "00:10:34.75", "00:10:56.80"
)

final_clip = CompositeVideoClip(
    [
        clip1,
    ]
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
    os.unlink(temp_audio_file.name)
except:
    pass

print("Video processing completed successfully!")
