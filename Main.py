import sys
import urllib
import requests
import Code.Getwavtime
import Code.Wavmerge
import Code.DeleteWav
import Code.tts
import Code.NoteExtraction


if __name__ == '__main__':
    ppt_path = input("请输入ppt所在的文件目录：")
    extension = ppt_path.split('.')[-1]  # 获取文件类型
    if extension == 'ppt':
        print('此ppt文件版本过低，请转换为pptx文件!')
        sys.exit()
    elif extension != 'pptx':  # 若为其他格式
        print('文件格式错误，请确保文件格式为pptx!')
        sys.exit()
    else:
        note = Code.NoteExtraction.ObtainPptNote(ppt_path)  # 获取备注
    if len(note) == 0:
        print('文件目录不能为空！')
        sys.exit()
    elif len(note) > 0:
        # print(note)
        x = 0
        time = []  # 获取各页备注的语音时间并存在列表中
        flag = False  # 标记是否有有效备注
        for i in range(len(note)):
            if len(note[i]) > 0:  # 有备注的话（可能有效可能无效）
                url = Code.tts.Synthesis(note[i])  # 获取url
                if url is not None:  # 避免无效备注的影响（无效备注无法生成语音）
                    urllib.request.urlretrieve(url, r"C:\Users\www22\Desktop\立项\备注提取\%s.wav" % x)   # 通过url下载音频并保存（绝对路径或相对路径都行）
                    second = Code.Getwavtime.GetTime(r"C:\Users\www22\Desktop\立项\备注提取\%s.wav" % x)  # 获取音频时长（单位为秒）
                    time.append(second)  # 加入时间列表
                    flag = True  # 代表存在有效备注
                else: time.append(0)
            else: time.append(0)
            x += 1
        # print(time)
        if flag:
            Code.Wavmerge.merge_files(r"C:\Users\www22\Desktop\立项\备注提取", r"C:\Users\www22\Desktop\立项\备注提取\output.wav")  # 第一个参数是wav文件所在的文件夹，第二个参数是保存路径
            Code.DeleteWav.Delete(r"C:\Users\www22\Desktop\立项\备注提取")  # 删除各段音频文件，只保留合并后的音频文件
        else:
            print('没有有效备注，无法生成语音！')
