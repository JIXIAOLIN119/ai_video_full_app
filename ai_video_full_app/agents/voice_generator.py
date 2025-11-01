from openai import OpenAI
import os

class VoiceGenerator:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, text, voice_name='alloy', language='中文'):
        file_path = f'./outputs/voice_{voice_name}_{hash(text)}.mp3'
        os.makedirs('./outputs', exist_ok=True)
        with self.client.audio.speech.with_streaming_response.create(model='gpt-4o-mini-tts', voice=voice_name, input=text) as response:
            response.stream_to_file(file_path)
        return file_path
