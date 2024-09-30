import edge_tts
import asyncio
from pydub import AudioSegment
import uuid
import os

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

class EdgeTTSConverter:
    def __init__(self, voice="zh-CN-XiaoxiaoNeural", rate="+0%", pitch="+0Hz"):
        """
        初始化类时设置默认语音、语速和音调
        :param voice: 语音类型，默认为 'zh-CN-XiaoxiaoNeural'
        :param rate: 语速，默认为 '0%'
        :param pitch: 音调，默认为 '0Hz'
        """
        self.voice = voice
        self.rate = rate
        self.pitch = pitch

    async def convert_text_to_wav(self, text, wav_file):
        """
        将文本转换为语音并保存为 WAV 文件
        :param text: 要转换的文本
        :param wav_file: 输出的 WAV 文件路径
        """
        temp_mp3_file = f"{uuid.uuid4()}.mp3"
        
        # 生成 MP3 文件
        communicate = edge_tts.Communicate(text, voice=self.voice, rate=self.rate, pitch=self.pitch)
        await communicate.save(temp_mp3_file)
        print(f"生成的 MP3 文件已保存为: {temp_mp3_file}")
        
        # 将 MP3 转换为 WAV
        sound = AudioSegment.from_mp3(temp_mp3_file)
        sound.export(wav_file, format="wav")
        os.remove(temp_mp3_file)
        print(f"生成的 WAV 文件已保存为: {wav_file}")

# 示例使用
if __name__ == "__main__":
    add_ffmpeg_to_path(ffmpeg_path)

    text = "你好，这是一个将文本转换为语音并生成 WAV 文件的示例。"
    wav_file = "output.wav"

    tts_converter = EdgeTTSConverter()

    # 异步生成 WAV 文件
    asyncio.run(tts_converter.convert_text_to_wav(text, wav_file))
