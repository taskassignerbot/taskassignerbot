import os
import speech_recognition as sr
import soundfile as sf
import tempfile
from transformers import pipeline

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
        return recognize_text_from_voice_temp(wav_file_path)

def recognize_text_from_voice(file_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(file_path) as source:
        audio = recognizer.record(source)
    text = recognizer.recognize_sphinx(audio)
    return text

# глеб, вот эту можешь функцию вообще убрать, только в process_voice_file_and_get_text поменяй на нужную
def recognize_text_from_voice_temp(file_path):
    pipe = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-100h")
    ans = pipe(file_path)
    return ans