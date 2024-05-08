import os
import speech_recognition as sr
import soundfile as sf
import tempfile
from transformers import pipeline
import assemblyai as aai

def convert_to_wav(voice):
    voice.download('file.ogg')
    data, samplerate = sf.read('file.ogg')
    sf.write('file.wav', data, samplerate)
    result = sf.read('file.wav')
    return result


async def process_voice_file_and_get_text(voice_file):
    with tempfile.TemporaryDirectory() as temp_dir:
        ogg_file_path = os.path.join(temp_dir, "voice_message.ogg")
        wav_file_path = os.path.join(temp_dir, "voice_message.wav")
        await voice_file.download_to_drive(custom_path=ogg_file_path)
        data, samplerate = sf.read(ogg_file_path)
        sf.write(wav_file_path, data, samplerate)
        return recognize_assembly(wav_file_path)

def recognize_text_from_voice(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_sphinx(audio)
    return text



def recognize_assembly(file_path): #РАБОЧИЙ ВАРИАНТ
    aai.settings.api_key = get_assemblyai_api_key()
    config = aai.TranscriptionConfig(
    word_boost=["Gleb", "Danil Petrov"],
    boost_param="high",
    language_code="ru",
    )
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(file_path)
    print(transcript.words)
    return transcript.text
