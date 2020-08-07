# merge_files_in_a_folder # 合并音频
import os
import glob
import numpy as np
import scipy.io.wavfile as wav


def merge_files(path_read_folder, path_write_wav_file):
    #
    files = os.listdir(path_read_folder)  # 返回指定路径下的文件和文件夹列表
    merged_signal = []
    for filename in glob.glob(os.path.join(path_read_folder, '*.wav')):  # 目标文件夹内的wav文件逐一进行操作
        # print(filename)
        if filename.split('\\')[-1] == 'output.wav':  # 规定output.wav是最后输出的音频文件，不对该wav文件进行合并
            continue
        sr, signal = wav.read(filename)  # 读取wav文件的信息
        merged_signal.append(signal)  # 添加到列表中
    merged_signal = np.hstack(merged_signal)  # 在水平方向上平铺
    merged_signal = np.asarray(merged_signal, dtype=np.int16)
    wav.write(path_write_wav_file, sr, merged_signal)  # 写入信息

"""
path_read_folder = "datasets/timit_noisy_selected/train/"
path_write_wav_file = "datasets/timit_noisy_selected_train_total.wav"
"""