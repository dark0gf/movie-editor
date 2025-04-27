from moviepy import *
import subprocess
import pysrt

text_clip_height_offset = 900

def process_subtitles(video_source, target_width, target_height):
    """
    Process subtitles and create text clips for each subtitle.
    
    Args:
        subtitles: List of subtitle objects from pysrt
        target_width: Width of the target video
        text_clip_height_offset: Vertical offset for positioning subtitles
        
    Returns:
        List of TextClip objects for all subtitles
    """

    # Subtitles extract
    temp_subtitle_file = './result/subtitles.srt'
    subtitle_command = [
        'ffmpeg',
        '-i', f'./video/{video_source}',
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

        # Create white text clip (English)
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

        # Create yellow text clip (Spanish)
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
    
    return subtitle_clips
