from moviepy import *
import subprocess
import pysrt
import re
import os
import deepl

text_clip_height_offset = 900

# Initialize DeepL translator
# You should set your DeepL API key as an environment variable: DEEPL_API_KEY
def get_translator():
    """
    Initialize and return a DeepL translator instance.
    
    Returns:
        deepl.Translator: A configured DeepL translator instance
    
    Raises:
        ValueError: If the DEEPL_API_KEY environment variable is not set
    """
    api_key = os.environ.get('DEEPL_API_KEY')
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is not set. Please set it to your DeepL API key.")
    
    return deepl.Translator(api_key)

def translate_text(text, target_lang='ES', source_lang=None):
    """
    Translate text using DeepL API.
    
    Args:
        text (str): Text to translate
        target_lang (str): Target language code (default: 'ES' for Spanish)
        source_lang (str, optional): Source language code. If None, DeepL will auto-detect.
    
    Returns:
        str: Translated text
        
    Example:
        >>> translate_text("Hello world", target_lang="ES")
        'Hola mundo'
    """
    try:
        translator = get_translator()
        result = translator.translate_text(
            text, 
            target_lang=target_lang,
            source_lang=source_lang
        )
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        # Return original text if translation fails
        return text

def time_to_seconds(time_str):
    """
    Convert time string in format HH:MM:SS.MS to seconds
    """
    # Check if time_str is already a number (seconds)
    if isinstance(time_str, (int, float)):
        return float(time_str)
    
    # Parse time string in format HH:MM:SS.MS
    pattern = r'(\d+):(\d+):(\d+)\.?(\d*)'
    match = re.match(pattern, time_str)
    
    if match:
        hours, minutes, seconds, milliseconds = match.groups()
        # Convert to seconds
        total_seconds = (int(hours) * 3600 + 
                         int(minutes) * 60 + 
                         int(seconds))
        
        # Add milliseconds if present
        if milliseconds:
            # Pad with zeros if needed
            milliseconds = milliseconds.ljust(3, '0')[:3]
            total_seconds += int(milliseconds) / 1000
            
        return total_seconds
    else:
        raise ValueError(f"Invalid time format: {time_str}")

def process_subtitles(video_source, subtitle_track, target_width, target_height, start_time, end_time):
    """
    Process subtitles and create text clips for each subtitle.
    
    Args:
        video_source: Source video file
        target_width: Width of the target video
        target_height: Height of the target video
        start_time: Start time of the clip (format: HH:MM:SS.MS)
        end_time: End time of the clip (format: HH:MM:SS.MS)
        
    Returns:
        List of TextClip objects for all subtitles within the time range
    """
    # Convert start_time and end_time to seconds
    clip_start_seconds = time_to_seconds(start_time)
    clip_end_seconds = time_to_seconds(end_time)
    
    print(f"Processing subtitles from {clip_start_seconds}s to {clip_end_seconds}s")

    # Subtitles extract
    temp_subtitle_file = './result/subtitles.srt'
    subtitle_command = [
        'ffmpeg',
        '-i', f'./video/{video_source}',
        '-map', f'0:s:{subtitle_track}',
        '-c', 'copy',
        '-y',
        temp_subtitle_file
    ]
    subprocess.run(subtitle_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # Subtitles clips
    subtitles = pysrt.open(temp_subtitle_file)

    subtitle_clips = []
    
    for sub in subtitles:
        sub_start_seconds = sub.start.ordinal / 1000  # Convert to seconds
        sub_end_seconds = sub.end.ordinal / 1000

        print(f"sub_start_seconds {sub_start_seconds} sub_end_seconds {sub_end_seconds}")
        
        # Skip subtitles outside the clip time range
        if sub_end_seconds < clip_start_seconds or sub_start_seconds > clip_end_seconds:
            continue
            
        # Adjust subtitle timing relative to the clip start time
        relative_start = max(0, sub_start_seconds - clip_start_seconds)
        relative_end = min(clip_end_seconds - clip_start_seconds, sub_end_seconds - clip_start_seconds)
        duration = relative_end - relative_start

        # Get the actual subtitle text
        subtitle_text = sub.text
        
        # Translate the subtitle text to Spanish using DeepL API
        translated_text = translate_text(subtitle_text, target_lang='ES')
        
        print(f"Original: '{subtitle_text}'")
        print(f"Translated: '{translated_text}'")
        
        # Create white text clip (English)
        text_clip_white = (
            TextClip(
                "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
                text=subtitle_text,
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
            .with_start(relative_start)
            .with_duration(duration)
        )

        text_clip_white = (
            TextClip(
                "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
                text=subtitle_text,
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
            .with_start(relative_start)
            .with_duration(duration)
        )

        print(f"Subtitle at {relative_start}s to {relative_end}s: '{subtitle_text}'")
        print(f"text_clip_white dimensions: {text_clip_white.size}")

        # Create yellow text clip with Spanish translation
        text_clip_yellow = (
            TextClip(
                "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
                text=translated_text,  # Using the translated text
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
            .with_start(relative_start)
            .with_duration(duration)
        )

        text_clip_yellow = (
            TextClip(
                "./fonts/Noto_Sans/static/NotoSans-Medium.ttf",
                text=translated_text,  # Using the translated text
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
            .with_start(relative_start)
            .with_duration(duration)
        )

        print(f"text_clip_yellow dimensions: {text_clip_yellow.size}")

        subtitle_clips.extend([text_clip_white, text_clip_yellow])
    
    print(f"Found {len(subtitle_clips) // 2} subtitles within the time range")
    return subtitle_clips
