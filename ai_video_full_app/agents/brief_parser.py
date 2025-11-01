from openai import OpenAI
import json

class BriefParser:
    def __init__(self):
        self.client = OpenAI()
    def parse(self, text):
        prompt = f"请将以下Brief转化为JSON：{text}"
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[{"role":"user","content":prompt}]
        )
        return json.loads(response.choices[0].message.content)
