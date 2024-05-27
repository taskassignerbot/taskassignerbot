import os
import speech_recognition as sr
import soundfile as sf
import tempfile
import assemblyai as aai
from api_keys import get_assemblyai_api_key, get_deepseek_key
from openai import OpenAI


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
    language_code="en",
    )
    transcriber = aai.Transcriber(config=config)
    transcript = transcriber.transcribe(file_path)
    print(transcript.words)
    print(transcript.text)
    return transcript.text

def paraphrase_message(message):
    client = OpenAI(api_key=get_deepseek_key(), base_url="https://api.deepseek.com")
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": f"'{message}' rewrite it to adress an adressee, here is an example: 'Tell Polina that her work is not bad, but she needs to make some corrections and then print it and bring it to me to morrow at 06:00 a.m' -> 'Polina, your work is quite good, but please make the necessary corrections. Afterward, print the document and deliver it to me tomorrow at 6:00 a.m.'"},
    ],
        max_tokens=128,
        temperature=1.2,
        frequency_penalty=-1.9,
        stream=False
    )

    return response.choices[0].message.content
