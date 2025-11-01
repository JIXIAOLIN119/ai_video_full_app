from openai import OpenAI
import json

class StoryboardGenerator:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, structured_brief, director_style="Apple 极简"):
        prompt = f"根据Brief生成分镜，导演风格:{director_style} {structured_brief}"
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[{"role":"user","content":prompt}]
        )
        return json.loads(response.choices[0].message.content)
