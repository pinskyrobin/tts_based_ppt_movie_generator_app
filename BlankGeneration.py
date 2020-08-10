#coding=utf-8
import os

def blank(time, file_path):
    cmd = "MKWav-7FH " + str(time * 1000) + " " + file_path  # 1000是把秒转换成毫秒为单位
    os.system(cmd)

#demo
# blank(18, r"C:\Users\www22\Desktop\立项\备注提取\km10.wav")  # 第一个参数代表多少秒