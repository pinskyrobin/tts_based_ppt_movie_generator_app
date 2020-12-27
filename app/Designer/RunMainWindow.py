from Designer.MainWindow import Ui_MainWindow
from Designer.Edit import Ui_SetTimeWindow
from Designer.BackConfirmWindow import Ui_BackConfirmWindow
from Designer.NoTimeConfirm import Ui_NoTimeConfirmWindow
from Designer.QuitWindow import Ui_FinishWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QDesktopWidget
from PyQt5.Qt import QThread, pyqtSignal
import sys
import VideoGenerator
import os
import pyaudio
import wave
import PyQt5.sip

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

class PreviewThread(QThread):
    _previewsignal = pyqtSignal()

    def __init__(self):
        super().__init__()

    def __del__(self):
        self.wait()

    def run(self):
        preview()
        self._previewsignal.emit()


class RunMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RunEdit(QWidget, Ui_SetTimeWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RunBack(QDialog, Ui_BackConfirmWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RunConfirmTime(QDialog, Ui_NoTimeConfirmWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class RunFinish(QDialog, Ui_FinishWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 选择主播ID
def chooseID():
    if mainWindow.ChooseGender.currentText() == '男声':
        mainWindow.ChooseSpeakerId.clear()
        mainWindow.ChooseSpeakerId.addItems(mainWindow.dict['male'])
    else:
        mainWindow.ChooseSpeakerId.clear()
        mainWindow.ChooseSpeakerId.addItems(mainWindow.dict['female'])


def previewClicked():
    mainWindow.PreviewButton.setEnabled(False)
    mainWindow.thread1 = PreviewThread()
    mainWindow.thread1._previewsignal.connect(mainWindow.set_PreviewButton)
    mainWindow.thread1.start()


# 试听函数
def preview():
    CHUNK = 1024
    if mainWindow.ChooseGender.currentText() == '男声':
        speaker_id = mainWindow.dict_male[mainWindow.ChooseSpeakerId.currentText()]
    else:
        speaker_id = mainWindow.dict_female[mainWindow.ChooseSpeakerId.currentText()]

    audio_name = os.path.join(os.getcwd(), "audio_src", str(speaker_id) + ".wav")
    wf = wave.open(audio_name, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    data = wf.readframes(CHUNK)
    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)
    stream.stop_stream()
    stream.close()
    p.terminate()


# 显示Edit界面
def showWindow():
    # 如果用户成功输入目标pptx文件与视频保存路径
    if mainWindow.convert():
        if mainWindow.update:
            VideoGenerator.imgGenerator(mainWindow.getFileDir(), os.path.join(os.getcwd(), 'pics'))
        mainWindow.hide()
        # 设置窗口居中
        qr = editWindow.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        editWindow.move(qr.topLeft())

        editWindow.show()
        editWindow.setDir(mainWindow.getFileDir(), mainWindow.getSaveDir())
        editWindow.process(mainWindow)


# 从Edit窗口返回至主窗口
def back():
    backWindow.exec_()
    backWindow.buttonBox.accepted.connect(backWindow.hide)
    backWindow.buttonBox.accepted.connect(editWindow.hide)
    backWindow.buttonBox.accepted.connect(mainWindow.show)

    backWindow.buttonBox.rejected.connect(backWindow.hide)
    backWindow.buttonBox.rejected.connect(editWindow.hide)
    backWindow.buttonBox.rejected.connect(mainWindow.show)
    backWindow.buttonBox.rejected.connect(initial)


# 取消保存后初始化变量
def initial():
    global is_final
    is_final = False
    editWindow._file_dir = ''
    editWindow._save_dir = ''
    editWindow.page = 1  # 当前幻灯片所在页数
    editWindow.notes = []  # 备注列表
    editWindow._pinyin = []  # 存储备注的拼音
    editWindow._time = []  # 存储每页幻灯片备注生成音频的秒数
    editWindow._gender = '1'  # 默认男声
    editWindow._gender_opt = '100453'  # 默认主播ID
    editWindow._is_pinyin_check = False  # 是否启用了拼音检查
    editWindow.is_no_notes_only = False  # 是否只查看无备注
    editWindow._no_notes_page = 0  # [只查看无备注页]模式的索引
    editWindow._no_notes = []  # 记录无备注幻灯片的页数位置


# 确认是否需要弹出0s确认窗口,并进行翻页操作
def confirm(re=False):
    global reverse
    reverse = re
    if editWindow.DisplayTime.value() == 0 and editWindow.notes[editWindow.page - 1] == '\n':
        confirmTimeWindow.exec_()
    else:
        turnPage()


# 点击[修改完成]后的确认函数
def confirmFinal():
    if editWindow.DisplayTime.value() == 0 and editWindow.notes[editWindow.page - 1] == '\n':
        global is_final
        is_final = True
        confirmTimeWindow.exec_()
    else:
        editWindow.download(finishWindow)


# 翻页函数,确认翻页的模式
def turnPage():
    QApplication.processEvents()
    global is_final
    if is_final:
        is_final = False
        editWindow.download(finishWindow)
    elif editWindow.is_no_notes_only:
        editWindow.displayNoNotes(reverse)
    else:
        editWindow.display(reverse)


def openVideo():
    os.startfile(os.path.join(mainWindow.getSaveDir(), "video.mp4"))


def quitWindow():
    mainWindow.close()
    editWindow.close()
    backWindow.close()
    confirmTimeWindow.close()
    finishWindow.close()


if __name__ == '__main__':
    reverse = False
    is_final = False
    app = QApplication(sys.argv)
    mainWindow = RunMain()
    editWindow = RunEdit()
    backWindow = RunBack()
    confirmTimeWindow = RunConfirmTime()
    finishWindow = RunFinish()
    mainWindow.show()

    # mainWindow窗口
    # 修改主播性别触发事件
    mainWindow.ChooseGender.currentIndexChanged.connect(chooseID)
    # 点击[试听]触发事件
    mainWindow.PreviewButton.clicked.connect(previewClicked)
    # 点击[开始转换]触发事件
    # editWindow窗口
    mainWindow.ConvertButton.clicked.connect(showWindow)
    # 点击[返回主界面]触发事件
    editWindow.BackButton.clicked.connect(back)
    # 点击[下一张]或[上一张]触发事件
    editWindow.PreSlideButton.clicked.connect(lambda: confirm(True))
    editWindow.NextSlideButton.clicked.connect(confirm)
    # 点击[修改完成]触发事件
    editWindow.CompleteButton.clicked.connect(confirmFinal)
    # 返回上层继续编辑空白备注停留时间
    confirmTimeWindow.buttonBox.rejected.connect(confirmTimeWindow.hide)
    # 确认该页空白幻灯片停留时间为0s
    confirmTimeWindow.buttonBox.accepted.connect(confirmTimeWindow.hide)
    confirmTimeWindow.buttonBox.accepted.connect(turnPage)

    # finishWindow窗口
    # 点击[打开视频]按钮触发事件
    finishWindow.OpenVideoButton.clicked.connect(openVideo)
    finishWindow.OpenVideoButton.clicked.connect(editWindow.hide)
    # 点击[返回主界面]按钮触发事件
    finishWindow.BackButton.clicked.connect(mainWindow.show)
    finishWindow.BackButton.clicked.connect(editWindow.hide)
    finishWindow.BackButton.clicked.connect(finishWindow.hide)
    # 点击[打开视频]或[退出]按钮触发事件
    finishWindow.OpenVideoButton.clicked.connect(quitWindow)
    finishWindow.QuitButton.clicked.connect(quitWindow)

    sys.exit(app.exec_())
