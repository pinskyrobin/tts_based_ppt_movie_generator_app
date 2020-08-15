#coding=utf-8
# 异常处理
import subprocess

Source_path = r"D:\项目\venv\Code\MKWav-7FH.exe "  # 命令行可执行文件的绝对路径

# 命令行
def blank(time, file_path):  # time是空白音频的时间（秒）
    try:
        cmd = Source_path + str(time * 1000) + " " + file_path  # 1000是把秒转换成毫秒为单位
        res = subprocess.call(cmd, shell=True)  # 命令行

        if res != 0:
            return False
        return True
    except Exception:
        return False


#demo
# blank(18, r"C:\Users\www22\Desktop\立项\备注提取\0.wav")