# merge_files_in_a_folder # 合并音频
from pydub import AudioSegment

def merge(path_read_folder, path_write_wav_file, len):
    input_music_0 = AudioSegment.from_wav(path_read_folder + r"\0.wav")  # 第一页ppt的音频
    for i in range(1, len):
        input_music = AudioSegment.from_wav(path_read_folder + r"\%s.wav" % i)
        input_music_0 = input_music_0 + input_music  # 循环连接所有音频
    input_music_0.export(path_write_wav_file, format="wav")  # 前面是保存路径，后面是保存格式

# demo
# merge(r"C:\Users\www22\Desktop\立项\备注提取", r"C:\Users\www22\Desktop\立项\备注提取\output.wav", 5)