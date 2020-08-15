# 音频名最好不带中文，wav文件过大的话可以采用原生变速（原生转换较慢）
# 异常处理
import subprocess

Source_path = r"D:\项目\venv\Code\ffmpeg.exe"  # 命令行可执行文件的绝对路径

# 原生（可能较慢）
def Prichange(audio_input, speed, audio_output):
    try:
        cmd = Source_path + " -n -i " + audio_input + " -filter:a atempo=%s " % speed + audio_output  # 第二个字符串那里atempo的值是倍速
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False

# 音频过大可能会运行失败
def a_speed(input_file, speed, out_file):
    try:
        cmd = Source_path + " -y -i %s -filter_complex \"atempo=tempo=%s\" %s" % (input_file, speed, out_file)  # 第二个参数填倍速
        res = subprocess.call(cmd, shell=True)

        if res != 0:
            return False
        return True
    except Exception:
        return False


# demo
# input = r"C:\Users\www22\Desktop\立项\备注提取\output.wav"
# output = r"C:\Users\www22\Desktop\立项\备注提取\output3x.wav"
# a_speed(input, 2, output)  # 两种方式
# Prichange(input, 2, output)