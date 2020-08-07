'''
################
# TTS 系统说明  #
################

url:		'http://111.230.90.48:8080/tts'
method: 	POST
data:		包含内容见下面示例
response:	'http://111.230.90.48:8080/' + src_0 即为合成的音频地址，可下载
'''

import json
import requests

# 通过文本合成语音
def Synthesis(Syntext):
    url = 'http://111.230.90.48:8080/tts'  # 可以先在浏览器打开，听听不同主播的效果

    # 一般情况下，只需设定 token text gender speaker_id
    parameter = {
        'token': 'asdfgh',  # 可以自己设定任意字符串
        'mode': '#synth_text',  # 从文本合成的模式
        'text': Syntext,  # 这里输入要合成的文本
        'pinyin': '',  # 拼音合成时输入
        'gender': '1',  # 女声为0，男声为1,与主播性别相匹配
        'speaker_id': '100453',  # 主播id
        'type': 'wav',  # 暂不支持mp3
    }
    # 如果文本较长，timeout要设定大一点
    response = requests.post(url, data=json.dumps(parameter), timeout=1000)

    if response.status_code == 200:
        data = response.json()
        info = data['info']
        src_0 = data['src_0']
        wav_url = 'http://111.230.90.48:8080/' + src_0  # 合成的音频文件地址
        print(info)
        return wav_url


# 通过拼音合成（拼音检查模式）
def pinyinSyn(Synpinyin):
    url = 'http://111.230.90.48:8080/tts'  # 可以先在浏览器打开，听听不同主播的效果

    # 一般情况下，只需设定 token text gender speaker_id
    parameter = {
        'token': 'asdfgh',  # 可以自己设定任意字符串
        'mode': '#synth_pinyin',  # 从拼音合成的模式
        'text': '',  # 这里输入要合成的文本
        'pinyin': Synpinyin,  # 拼音合成时输入
        'gender': '1',  # 女声为0，男声为1,与主播性别相匹配
        'speaker_id': '100453',  # 主播id
        'type': 'wav',  # 暂不支持mp3
    }
    # 如果文本较长，timeout要设定大一点
    response = requests.post(url, data=json.dumps(parameter), timeout=1000)

    if response.status_code == 200:
        data = response.json()
        info = data['info']
        src_0 = data['src_0']
        wav_url = 'http://111.230.90.48:8080/' + src_0  # 合成的音频文件地址
        print(info)
        return wav_url
    """print(text)
    print(pinyin)
    print(info)

    # 多音字问题 临时解决方案：
    # 1. response 有反馈 text 和 pinyin， 可以给用户提供拼音修改功能
    # 2. 将修改后的拼音 放入parameter 中的 'pinyin', 并将 'mode' 改成 '#synth_pinyin'
    # 例如：  parameter['pinyin']='di4 yi1 hang2 .' parameter[mode]='#synth_pinyin'
    # 3. 拼音模式重新合成"""