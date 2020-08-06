from time import sleep
from os import listdir
from os.path import join, splitext, dirname
from shutil import rmtree
from re import findall
from win32com.client import gencache, Dispatch
from moviepy.editor import (AudioFileClip,
                            ImageSequenceClip,
                            concatenate_audioclips)

# 要转换的ppt文件
ppt_fn = r''  # 单引号里面是绝对路径(.pptx或.ppt)
# 临时存放拆分后的幻灯片的文件夹
picture_dir = splitext(ppt_fn)[0] + '_pictures'  # 单引号里面是啥不知道
# 背景音乐（合成的语音的音频文件）
audio_fn = r''  # 单引号里面是绝对路径(.wav)

# 把ppt转换为图片，每个幻灯片一个图片文件
powerpoint = Dispatch('PowerPoint.Application')  # 参数未知
powerpoint.Visible = True
ppt1 = powerpoint.Presentations.Open(ppt_fn)
gencache.EnsureDispatch('PowerPoint.Application')
ppt1.SaveAs(f'{pictures_dir}.jpg', 17)  # 参数应该要改
ppt1.Close()
if not powerpoint.Presentations:
    powerpoint.Quit()

# 对图片按幻灯片编号进行排序
pictures = [join(pictures_dir, fn)
            for fn in listdir(pictures_dir)
            if fn.endswith(',jpg')]
pictures.sort(key=lambda fn: int(findall(r'\d+', fn)[-1]))

# 音乐重复播放两次（这里应该要改）
audio = concatenate_audioclips([AudioFileClip(audio_fn)] * 2)

# 计算每个幻灯片图片在视频中停留的时长（这个应该也要改）
num = len(pictures)
durations = [float(str(audio.duration / num)[:4])] * num

# 根据给定的图片序列生成视频，设置音频，写入视频文件(应该要改)
(ImageSequenceClip(pictures,
                   durations=durations)
 .set_audio(audio)
 .write_videofile(rf'{splitext(ppt_fn)[0]}_video.mp4',
                  codec='libx264', fps=24))    # 生成mp4文件（可调帧率）

# 删除临时生成的图片文件
rmtree(pictures_dir)
