import contextlib
import wave

# 获取音频时长
def GetTime(file_path):
    # file_path = r"C:\Users\www22\Desktop\立项\备注提取\code.wav"   双引号内填绝对路径（.wav）
    with contextlib.closing(wave.open(file_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        wav_length = frames / float(rate)
        return wav_length  # 单位为秒