# 两种转换方式应该都行，相差不大，都是命令行

# 音频名最好不带中文，wav文件过大的话可以采用原生变速（原生转换较慢）
import os

def Prichange(audio_input, audio_output):
    cmd = "ffmpeg -n -i " + audio_input + " -filter:a atempo=0.5 " + audio_output  # 第二个字符串那里atempo的值是倍速
    # print(cmd)
    os.system(cmd)  # 命令行操作


# wav文件较小时使用
import subprocess

def a_speed(input_file, speed, out_file):
    try:
        cmd = "ffmpeg -y -i %s -filter_complex \"atempo=tempo=%s\" %s" % (input_file, speed, out_file)  # 第二个参数填倍速
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# demo
input = r"C:\Users\www22\Desktop\立项\备注提取\output.wav"
output = r"C:\Users\www22\Desktop\立项\备注提取\output5x.wav"
# a_speed(input, 2, output)  # 两种方式
Prichange(input, output)