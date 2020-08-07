import os
import glob


def Delete(path_read_folder):
    # path = imgDate_listResult
    files = os.listdir(path_read_folder)  # 返回指定路径下的文件和文件夹列表
    for infile in glob.glob(os.path.join(path_read_folder, '*.wav')):
        if infile.split('\\')[-1] != 'output.wav':  # 最终输出音频不删除
            os.remove(infile)  # 删除