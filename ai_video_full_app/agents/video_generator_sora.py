import requests, time

class SoraVideoGenerator:
    def __init__(self, endpoint, api_key):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.headers = {'Content-Type':'application/json','api-key':self.api_key}
    def create_video(self, prompt, width=480, height=480, duration=5, model='sora'):
        url = f'{self.endpoint}/openai/v1/video/generations/jobs?api-version=2024-09-01-preview'
        payload = {'model':model,'prompt':prompt,'width':width,'height':height,'n_seconds':duration}
        resp = requests.post(url, headers=self.headers, json=payload)
        resp.raise_for_status()
        job = resp.json()
        job_id = job['id']
        status = None
        while status not in ('succeeded','failed'):
            time.sleep(3)
            poll = requests.get(f'{self.endpoint}/openai/v1/video/generations/jobs/{job_id}', headers=self.headers, params={'api-version':'2024-09-01-preview'})
            poll.raise_for_status()
            status = poll.json().get('status')
        if status=='succeeded':
            return poll.json()['result']['output'][0]['url']
        else:
            raise Exception(f'Sora 视频生成失败: {poll.json()}')
