from gtts import gTTS
import os
from datetime import datetime

# A temporary directory to store the generated audio files.
# In a real production app, this might be a cloud storage bucket (like S3).
AUDIO_OUTPUT_DIR = "temp_audio"

def convert_text_to_audio(text_to_convert: str) -> str | None:
    """
    Converts a string of text into an MP3 audio file using gTTS.

    Args:
        text_to_convert: The text to be converted to speech.

    Returns:
        The file path to the generated MP3 file, or None if an error occurred.
    """
    if not text_to_convert:
        return None

    try:
        # Ensure the output directory exists.
        os.makedirs(AUDIO_OUTPUT_DIR, exist_ok=True)

        # Create the gTTS object. lang='es' for Spanish.
        # We set slow=False for a natural speaking rate.
        tts = gTTS(text=text_to_convert, lang='es', slow=False)

        # Generate a unique filename to avoid conflicts.
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        filename = f"homework_{timestamp}.mp3"
        filepath = os.path.join(AUDIO_OUTPUT_DIR, filename)

        # Save the audio file
        tts.save(filepath)

        print(f"Audio file generated successfully: {filepath}")
        return filepath

    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")
        return None
