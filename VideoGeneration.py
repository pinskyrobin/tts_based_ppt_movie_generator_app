from time import sleep
from os import listdir
from os.path import join, splitext, dirname
from shutil import rmtree
from re import findall
from win32com.client import gencache, Dispatch
from moviepy.editor import *

# ppt所在路径， wav音频所在路径， mp4视频输出路径， 时间序列
def video(ppt_fn, wav_path, final_video_path, time):
    # 要转换的ppt文件
    # ppt_fn = r'C:\Users\www22\Desktop\立项\备注提取\demo.pptx'  # 单引号里面是绝对路径(.pptx或.ppt)
    # 临时存放拆分后的幻灯片的文件夹，新建存放每页ppt截图的文件夹
    pictures_dir = splitext(ppt_fn)[0] + '_pictures'  # 等号右边第一个是文件名(去除扩展名)

    # 把ppt转换为图片，每个幻灯片一个图片文件
    powerpoint = Dispatch('PowerPoint.Application')
    powerpoint.Visible = True
    ppt1 = powerpoint.Presentations.Open(ppt_fn)  # ppt实例对象
    gencache.EnsureDispatch('PowerPoint.Application')
    ppt1.SaveAs(f'{pictures_dir}.jpg', 17)  # 保存图片
    ppt1.Close()
    if not powerpoint.Presentations:
        powerpoint.Quit()  # 退出ppt

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
    # demo
    # wav_path = r"C:\Users\www22\Desktop\立项\备注提取\output.wav"
    # final_video_path = r"C:\Users\www22\Desktop\立项\备注提取\output233.mp4"
    wav_clip = AudioFileClip(wav_path)
    result_video = result_video.set_audio(wav_clip)
    result_video.write_videofile(final_video_path, fps = 24)  # 保存mp4视频，帧率24

    # 删除临时生成的文件夹
    rmtree(pictures_dir)