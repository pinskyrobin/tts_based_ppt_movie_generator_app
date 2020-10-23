from os import path, walk, remove
import os
from pydub import AudioSegment


# 获取上级目录:os.path.abspath(os.path.join(os.getcwd(), ".."))
# 获取当前目录:os.getcwd(), os.path.abspath(os.path.dirname(__file__))


# 生成空白音频文件
def BlankAudio(time, file_path):
    if time == 0:
        return
    duration = AudioSegment.silent(duration=time * 1000)
    duration.export(file_path, format="wav")


# 合并音频文件
def MergeAudio(folder, target_file, file_num, zero, exist):
    total = AudioSegment.empty()
    first = AudioSegment.from_wav(os.path.abspath(os.path.join(os.getcwd(), "audio_src", "000000.wav")))
    for i in range(file_num):
        if i in zero:
            continue
        piece = AudioSegment.from_wav(path.join(folder, "%s.wav" % (i + 1)))
        if i in exist:
            total = total + first + piece
        else:
            total = total + piece
    total.export(target_file, format="wav")


# 删除音频片段
def DeleteAudio():
    for root, dirs, files in walk(os.getcwd()):
        for file in files:
            if file.split('.')[-1] == 'wav' and len(file.split('.')[0]) <= 5:
                remove(path.join(os.getcwd(), file))
