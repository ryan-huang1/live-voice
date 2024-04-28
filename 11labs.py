from elevenlabs.client import ElevenLabs
from elevenlabs import Voice, VoiceSettings
from dotenv import load_dotenv
import os
import wave
import uuid  # For generating unique file names

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('11LABS_API_KEY')

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=api_key)

def generate_audio_file(text, directory='audio_files'):
    """
    Generates an audio file from the provided text using ElevenLabs API and saves it in the specified directory.
    
    Args:
    text (str): The text to be converted to speech.
    directory (str): The directory where the audio file will be saved.
    
    Returns:
    str: The filename of the saved audio file.
    """
    # Ensure the directory exists
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Generate a random UUID for the filename
    filename = f"{uuid.uuid4()}.wav"
    filepath = os.path.join(directory, filename)

    # Generate the audio content
    audio_generator = client.generate(
        model="eleven_turbo_v2",
        text=text,
        voice=Voice(
            voice_id='EaRGedvaEUcGKOARaf6W',
            settings=VoiceSettings(stability=0.71, similarity_boost=0.5, style=0.0, use_speaker_boost=True)
        )
    )

    # Save the audio to a file
    with wave.open(filepath, 'wb') as f:
        f.setnchannels(1)  # Mono channel
        f.setsampwidth(2)  # Sample width in bytes
        f.setframerate(24000)  # Frame rate
        
        for chunk in audio_generator:
            f.writeframes(chunk)

    return filepath

# Example usage
text_to_convert = '''In the heart of an ancient forest, a curious phenomenon occurs each year on the eve of the autumn equinox.'''
audio_filepath = generate_audio_file(text_to_convert)
print(f"Audio file saved as {audio_filepath}")
