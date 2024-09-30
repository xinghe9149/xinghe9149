import json
import os.path
import asyncio
from chat.client.chat_client import ChatClientWithSQLite
from chat.client.responses import ChatResponse
from chat.data.entity import Message
from langchain_community.llms import Ollama
from tts_stt_local.tts_byedge import EdgeTTSConverter
def add_ffmpeg_to_path(ffmpeg_path):
    # 获取当前的 PATH 环境变量
    current_path = os.environ.get('PATH', '')
    
    # 将 ffmpeg 路径添加到 PATH
    if ffmpeg_path not in current_path:
        os.environ['PATH'] = ffmpeg_path + os.pathsep + current_path
        print(f"FFmpeg 路径 {ffmpeg_path} 已添加到环境变量 PATH 中")
    else:
        print(f"FFmpeg 路径 {ffmpeg_path} 已经在环境变量 PATH 中")

# ffmpeg 安装路径
ffmpeg_path = r'ffmpeg-6.1.1-full_build-shared\bin'  # 替换为你 ffmpeg 的实际安装路径

# 调用函数将 ffmpeg 添加到 PATH

class ollama_myself(ChatClientWithSQLite):
    API_KEY: str
    SECRET_KEY: str
    KEY_SRC = "role"
    KEY_CONTENT = "content"
    EdgeTTS = EdgeTTSConverter
    MODEL: str = "qwen2:latest"
    API: str = "https:localhost:11434"
    VALUE_USER = "user"
    VALUE_ASSISTANT = "assistant"
    access_token: str = ""
    expire_at: int = 0
    def __init__(self,  key_src: str, key_content: str):
        super().__init__('ollama', 'role', 'content')
        self.API_KEY = key_src
        self.SECRET_KEY = key_content
        self.host = "localhost"
        self.port = "11434"
        self.MODEL = "qwen2"
        self.wav_output_path = "test_output.wav"
        self.EdgeTTS = EdgeTTSConverter()
        add_ffmpeg_to_path(ffmpeg_path)
    def chat(self,text):
        Message.create(chatId=self.config.chatId.value, dst=self.VALUE_ASSISTANT, src=self.VALUE_USER, text=text)
        self.messages.append({
            "role": self.VALUE_USER,
            "content": text
        })

        try:
            res = self.__ollama_chat()
        except Exception as e:
            res = str(e)

        self.messages.append({
            'role': self.VALUE_ASSISTANT,
            'content': res
        })
        asyncio.run(self.EdgeTTS.convert_text_to_wav(res, 'test_output.wav'))
        Message.create(chatId=self.config.chatId.value, src=self.VALUE_ASSISTANT, dst=self.VALUE_USER, text=res)

        return ChatResponse({'text': res,'audio':'test_output.wav'})
    def __ollama_chat(self):
        messages=self.getCharaSetting() + self.messages
        temperature = 0.9,
        llm = Ollama(base_url=f"http://{self.host}:{self.port}",model = self.MODEL)
        res = llm.invoke(messages)
        return res
    def loadMessages(self, chat_id: str):
        access_token_path = 'ollama_myself.json'

        if os.path.exists(access_token_path):
            with open(access_token_path, 'r', encoding='utf-8') as f:
                x = json.loads(f.read())
                self.access_token = x.get('access_token')
                self.expire_at = x.get('expire_at')

        return super().loadMessages(chat_id)