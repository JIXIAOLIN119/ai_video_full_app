from openai import OpenAI
import json

class VisualPromptAgent:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, storyboard_json):
        prompt = f"生成视觉提示词 {storyboard_json}"
        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[{"role":"user","content":prompt}]
        )
        return json.loads(response.choices[0].message.content)
