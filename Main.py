import sys
import urllib
import requests
import os
from shutil import rmtree
import Code.Getwavtime
import Code.Wavmerge
import Code.tts
import Code.NoteExtraction
import Code.BlankGeneration
import Code.VideoGeneration
import Code.SpeedRegulation


# 代码异常处理选用的是万能异常，具体异常名未知。可能会导致某些特殊异常无法正确处理。
# 拼音检查在此没有实现
if __name__ == '__main__':
    # 备注提取
    ppt_path = input("请输入PPT所在的文件目录：")
    extension = ppt_path.split('.')[-1]  # 获取文件类型
    if extension == 'ppt':
        print('此PPT文件版本过低，请转换为pptx文件!')
        sys.exit()
    elif extension != 'pptx':  # 若为其他格式
        print('文件格式错误，请确保文件格式为pptx!')
        sys.exit()
    else:
        try:
            note = Code.NoteExtraction.ObtainPptNote(ppt_path)  # 获取备注
        except Exception:
            print("不存在该pptx格式的文件，备注提取失败！")
            sys.exit()

    # 语音合成
    if len(note) == 0:
        print('PPT文件路径不能为空！')
        sys.exit()
    elif len(note) > 0:
        # print(note)
        wav_dir = os.path.splitext(ppt_path)[0] + '_wav'  # 等号右边第一个是文件名(去除扩展名)
        if not os.path.exists(wav_dir):  # 该文件夹不存在的话
            os.makedirs(wav_dir)  # 创建存放wav音频的文件夹
        x = 0
        time = []  # 获取各页备注的语音时间并存在列表中

        # 主播性别：男或女
        gender = input("请选择主播性别：")
        while gender != "男" or gender != "女":
            gender = input("输入错误，请重新选择主播性别：")

        # 主播id存放在字典中，键和值均为字符串型，分男主播、女主播两个字典
        man = {"磁性男声": "107289", "时尚男声": "100453",
               "浑厚男声": "106528", "成熟男声": "107813", "亲切男声": "blz"}
        woman = {"亲切女声": "101238", "时尚女声": "100438", "甜美女声": "108259-shaoyv",
                 "温柔女声": "100216", "活泼女声": "biaobei", "可爱女童": "108259-luoli"}
        name = input("请选择主播：")
        if gender == "男":
            gendernum = '1'
            while name not in man:
                name = input("该男主播不存在，请重新选择男主播：")
        if gender == "女":
            gendernum = '0'
            while name not in woman:
                name = input("该女主播不存在，请重新选择女主播：")

        # 是否启用拼音检查
        # check = False

        for i in range(len(note)):
            flag = False  # 标记这一页ppt是否有有效备注
            if len(note[i]) > 0:  # 有备注的话（可能有效可能无效）
                try:
                    url = Code.tts.Synthesis(note[i], speaker[name], gendernum)  # 获取url
                except Exception:
                    print("语音合成系统不能正常访问！")
                    rmtree(wav_dir)
                    sys.exit()
                if url is not None:  # 避免无效备注的影响（无效备注无法生成语音）
                    urllib.request.urlretrieve(url, wav_dir + r"\%s.wav" % x)   # 通过url下载音频并保存（绝对路径或相对路径都行）
                    second = Code.Getwavtime.GetTime(wav_dir + r"\%s.wav" % x)  # 获取音频时长（单位为秒）
                    time.append(second)  # 加入时间列表
                    flag = True  # 代表这一页备注是有效备注
            if not flag:  # 空白备注或无效备注的处理
                print("请为空白备注页%d选择空白音频时长：" % (i + 1))
                # duration = int(input())  # 每次都输入的话会比较慢
                duration = 1  # demo
                while duration < 0:
                    print("时长必须为正数！")
                    print("请重新为空白备注页%d选择空白音频时长：" % (i + 1))
                    duration = int(input())
                time.append(duration)
                res_1 = Code.BlankGeneration.blank(duration, wav_dir + r"\%s.wav" % x)  # 空白音频生成
                if not res_1:
                    print("空白音频生成失败！")
                    rmtree(wav_dir)
                    sys.exit()
            x += 1
        # 语音合并
        Code.Wavmerge.merge(wav_dir, wav_dir + r"\output1x.wav", len(time))  # wav文件所在的文件夹，保存路径，时间序列长度

        # 变速（播放速度范围：0.50~2.00，保留两位小数）
        # speed = input("请设置音频播放速度：")
        speed = 1 # demo
        while speed < 0.5 or speed > 2:
            print("播放速度范围：0.50~2.00")
            speed = input("请设置音频播放速度：")
        if speed != 1:
            # 文件名标注倍速
            res_2 = Code.SpeedRegulation.a_speed(wav_dir + r"\output1x.wav", speed, wav_dir + r"\output%sx.wav" % speed)
            if not res_2:
                res_3 = Code.SpeedRegulation.Prichange(wav_dir + r"\output1x.wav", speed, wav_dir + r"\output%sx.wav" % speed)
                if not res_3:
                    print("播放速度调节失败！")
                    rmtree(wav_dir)
                    sys.exit()
            for i in range(len(time)):
                time[i] = time[i] / speed

        # 视频合成，音量调整（volume的值代表是原音量的多少倍）
        final_path = r"C:\Users\www22\Desktop\立项\备注提取\output233.mp4"  # 最终视频保存的你路径
        # volume = input("清设置视频音量（1为标准）：")  # volume代表音量放大（减小）几倍
        volume = 1
        while volume < 0.5 or volume > 10:
            print("所选音量不合适！")
            volume = input("音频音量范围：0.5~10")

        Code.VideoGeneration.video(ppt_path, wav_dir + r"\output%sx.wav" % speed, final_path, time, volume)  # PPT文件所在路径，wav音频所在路径，mp4视频输出路径，时间序列，音量

        rmtree(wav_dir) # 删除临时文件夹
        # print(time)