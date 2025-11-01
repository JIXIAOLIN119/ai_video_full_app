import os
from openai import OpenAI

class BGMGenerator:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, style='Cinematic', duration=10):
        file_path = f'./outputs/bgm_{style}.mp3'
        os.makedirs('./outputs', exist_ok=True)
        with open(file_path,'wb') as f:
            f.write(b'')
        return file_path
