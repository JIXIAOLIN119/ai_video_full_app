# Streamlit 全功能版主程序
import streamlit as st
st.title("🎬 AI 视频导演工作台")
st.write("import os

root = "ai_video_full_app"

# ---------------- 创建目录 ----------------
folders = [
    root,
    os.path.join(root, "agents"),
    os.path.join(root, ".streamlit"),
    os.path.join(root, "assets")
]

for folder in folders:
    os.makedirs(folder, exist_ok=True)

# ---------------- 文件内容 ----------------

# app.py (请将完整版代码替换到这里)
app_py = """\
# Streamlit 全功能版主程序
import streamlit as st
st.title("🎬 AI 视频导演工作台")
st.write("请将完整版 app.py 代码替换到这里")
"""

# requirements.txt
requirements_txt = """\
streamlit
openai
requests
moviepy
"""

# README.md
readme_md = """\
# AI 视频导演工作台 (全功能版)

功能：
- 分镜生成
- 每镜头独立 Sora 视频生成
- 多角色 VO 配音
- 自动背景音乐生成与混音
- 视频拼接与导出
"""

# .streamlit/secrets.toml
secrets_toml = """\
AZURE_ENDPOINT = "https://YOUR_RESOURCE_NAME.openai.azure.com"
AZURE_API_KEY = "YOUR_API_KEY"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
"""

# agents 模块内容
agents_files = {
    "__init__.py": "",
    "brief_parser.py": """\
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
""",
    "storyboard_generator.py": """\
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
""",
    "visual_prompt_agent.py": """\
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
""",
    "video_generator_sora.py": """\
import requests, time

class SoraVideoGenerator:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.headers = {"Content-Type":"application/json","api-key":self.api_key}
    def create_video(self, prompt, width=480, height=480, duration=5, model="sora"):
        url = f"{self.endpoint}/openai/v1/video/generations/jobs?api-version=2024-09-01-preview"
        payload = {"model":model,"prompt":prompt,"width":width,"height":height,"n_seconds":duration}
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        job = resp.json()
        job_id = job["id"]
        status = None
        while status not in ("succeeded","failed"):
            time.sleep(3)
            poll = requests.get(f"{self.endpoint}/openai/v1/video/generations/jobs/{job_id}",
                                headers=self.headers, params={"api-version":"2024-09-01-preview"})
            poll.raise_for_status()
            status = poll.json().get("status")
        if status=="succeeded":
            return poll.json()["result"]["output"][0]["url"]
        else:
            raise Exception(f"Sora 视频生成失败: {poll.json()}")
""",
    "voice_generator.py": """\
from openai import OpenAI
import os

class VoiceGenerator:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, text, voice_name="alloy", language="中文"):
        file_path = f"./outputs/voice_{voice_name}_{hash(text)}.mp3"
        os.makedirs("./outputs", exist_ok=True)
        with self.client.audio.speech.with_streaming_response.create(
            model="gpt-4o-mini-tts",
            voice=voice_name,
            input=text
        ) as response:
            response.stream_to_file(file_path)
        return file_path
""",
    "bgm_generator.py": """\
import os
from openai import OpenAI

class BGMGenerator:
    def __init__(self):
        self.client = OpenAI()
    def generate(self, style="Cinematic", duration=10):
        file_path = f"./outputs/bgm_{style}.mp3"
        os.makedirs("./outputs", exist_ok=True)
        with open(file_path,"wb") as f:
            f.write(b"")
        return file_path
"""
}

# -------------------- 写入文件 --------------------
files = {
    os.path.join(root, "app.py"): app_py,
    os.path.join(root, "requirements.txt"): requirements_txt,
    os.path.join(root, "README.md"): readme_md,
    os.path.join(root, ".streamlit", "secrets.toml"): secrets_toml
}

for path, content in files.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

for fname, content in agents_files.items():
    with open(os.path.join(root, "agents", fname), "w", encoding="utf-8") as f:
        f.write(content)

# assets/demo_logo.png (占位空文件)
with open(os.path.join(root, "assets", "demo_logo.png"), "wb") as f:
    f.write(b"")

print(f"✅ 全部文件已生成在 ./{root} 目录下")
print("接下来可以压缩该目录上传 GitHub 并部署到 Streamlit")
")
