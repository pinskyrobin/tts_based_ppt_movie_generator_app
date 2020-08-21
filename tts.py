'''
################
# TTS 系统说明  #
################

url:		'http://111.230.90.48:9006/tts'
method: 	POST
data:		包含内容见下面示例
response:	'http://111.230.90.48:9006/' + src_0 即为合成的音频地址，可下载
'''

import json
import requests

# 通过文本合成语音
def Synthesis(Syntext, id, gendernum):
    url = 'http://111.230.90.48:9006/tts'  # 可以先在浏览器打开，听听不同主播的效果

    # 一般情况下，只需设定 token text gender speaker_id
    parameter = {
        'token': 'asdfgh',  # 可以自己设定任意字符串
        'mode': '#synth_text',  # 从文本合成的模式
        'text': Syntext,  # 这里输入要合成的文本
        'pinyin': '',  # 拼音合成时输入
        'gender': gendernum,  # 女声为0，男声为1,与主播性别相匹配
        'speaker_id': id,  # 主播id (demo:'100453')字符串类型
        'type': 'wav',  # 暂不支持mp3
    }
    # 如果文本较长，timeout要设定大一点
    response = requests.post(url, data=json.dumps(parameter), timeout=1000)

    if response.status_code == 200:
        data = response.json()
        info = data['info']
        src_0 = data['src_0']
        wav_url = 'http://111.230.90.48:9006/' + src_0  # 合成的音频文件地址
        print(info)  # 打印合成成功地信息
        return wav_url


# 通过拼音合成（拼音检查模式）
"""
print(text)
print(pinyin)
print(info)

# 多音字问题 临时解决方案：
# 1. response 有反馈 text 和 pinyin， 可以给用户提供拼音修改功能
# 2. 将修改后的拼音 放入parameter 中的 'pinyin', 并将 'mode' 改成 '#synth_pinyin'
# 例如：  parameter['pinyin']='di4 yi1 hang2 .' parameter[mode]='#synth_pinyin'
# 3. 拼音模式重新合成

# 主播id:

# 女主播 id：
100438
biaobei
dll
ljspeech
tx_f
wjh_zhufu
100117
100203
100216
101238
105706
111782
108259-luoli
108259-shaonv
108259-shaoyv

# 男主播 id
100453
blz
gudian
wxb
lx_b
lx_y
100027
100174
100242
100851
102468
105706
106528
107289
107813
110474
"""