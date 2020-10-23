from os import listdir
from os.path import join, splitext, dirname
from shutil import rmtree
from re import findall

import comtypes.client
from win32com import client
from moviepy.editor import *


# 结束后台的Powerpoint进程
def closesoft():
    wc = client.constants
    wps = client.gencache.EnsureDispatch('PowerPoint.Application')
    try:
        wps.Presentations.Close()
        wps.Quit()
    except:
        pass


# 将幻灯片转换为图片
def imgGenerator(ppt_fn, pictures_dir):
    closesoft()
    powerpoint = comtypes.client.CreateObject("PowerPoint.Application")
    powerpoint.Visible = True
    ppt = powerpoint.Presentations.Open(ppt_fn)
    ppt.SaveAs(pictures_dir + '.jpg', 17)
    ppt.Close()
    # powerpoint.Quit()


# 生成音频
def video(ppt_fn, wav_path, final_video_path, time):
    pictures_dir = os.path.join(os.getcwd(), 'pics')
    # 要转换的ppt文件
    # 临时存放拆分后的幻灯片的文件夹，新建存放每页ppt截图的文件夹
    # pictures_dir = splitext(ppt_fn)[0] + '_pictures'  # 等号右边第一个是文件名(去除扩展名)

    # 把ppt转换为图片，每个幻灯片一个图片文件

    # 对图片按幻灯片编号进行排序
    pictures = [join(pictures_dir, fn)
                for fn in listdir(pictures_dir)
                if fn.endswith('.JPG') or fn.endswith('.jpg')]  # 大小写虽然是一样的，但还是会区分
    pictures.sort(key=lambda fn: int(findall(r'\d+', fn)[-1]))  # 排序

    # 连接多个图片
    image = []
    i = 0
    for pic in pictures:
        image.append(ImageClip(pic,
                               duration=time[i]))
        i = i + 1
    result_video = concatenate_videoclips(image)  # 生成图片序列的视频

    # 设置背景音乐
    wav_clip = AudioFileClip(wav_path)
    result_video = result_video.set_audio(wav_clip)
    result_video.write_videofile(final_video_path, fps=24)  # 保存mp4视频，帧率24

    # 删除临时生成的文件夹
    rmtree(pictures_dir)
    os.remove(os.path.abspath(os.path.join(os.getcwd(), "..", "audio.wav")))
