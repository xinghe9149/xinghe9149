import json
import os.path
import time

import requests
from core.audio_device import AudioDevice
from core.lock import Lockable
from chat.client.chat_client import ChatClientWithSQLite
from chat.client.responses import ChatResponse
from chat.data.entity import Message
from utils import log
from langchain_community.llms import Ollama
from config import Configuration
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
import base64

class ollama_myself(ChatClientWithSQLite):
    API_KEY: str
    SECRET_KEY: str
    KEY_SRC = "role"
    KEY_CONTENT = "content"

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
class ollama_tts(AudioDevice):
    def __init__(self, volumeConfig: Configuration, onFinishCallback: callable):
        super().__init__(volumeConfig, onFinishCallback)
    pass