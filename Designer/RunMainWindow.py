import sys
from Designer import MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog

import NotesExtract
import tts
import requests
import urllib

file_dir = ' '
save_dir = ' '

_translate = QtCore.QCoreApplication.translate

MainWindow.Ui_MainWindow.ChooseFileButton.clicked.connect(MainWindow.Ui_MainWindow.openfile)
MainWindow.Ui_MainWindow.ChooseSavedDirButton.clicked.connect(MainWindow.Ui_MainWindow.savefile)
MainWindow.Ui_MainWindow.ConvertButton.clicked.connect(MainWindow.Ui_MainWindow.convert)


def openfile(self):
    openfile_name = QFileDialog.getOpenFileName(None, '选择文件', '', 'Pptx files(*.pptx)')
    MainWindow.Ui_MainWindow.file_dir = openfile_name[0]
    MainWindow.Ui_MainWindow.FileDirBlank.setText(MainWindow.Ui_MainWindow.file_dir)


def savefile(self):
    MainWindow.Ui_MainWindow.save_dir = QtWidgets.QFileDialog.getExistingDirectory(None, "getExistingDirectory", "./")
    MainWindow.Ui_MainWindow.SavedDirBlank.setText(MainWindow.Ui_MainWindow.save_dir)


def convert(self, MainWindow):
    if MainWindow.Ui_MainWindow.file_dir == ' ':
        # MainWindow.Ui_MainWindow.StatusLabel.setText("文件目录为空!请检查后重试!")
        MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" "
                                                 "font-size:14pt; color:#ff0000;\""
                                                 ">文件目录为空!请检查后重试!"
                                                 "</span></p></body></html>"))
        return
    if MainWindow.Ui_MainWindow.save_dir == ' ':
        # MainWindow.Ui_MainWindow.StatusLabel.setText("保存路径为空!请检查后重试!")
        MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" "
                                                 "font-size:14pt; color:#ff0000;\""
                                                 ">保存路径为空!请检查后重试!"
                                                 "</span></p></body></html>"))
        return
    if MainWindow.Ui_MainWindow.PinyinCheck.isChecked():
        MainWindow.Ui_MainWindow.resize(530, 510)
    MainWindow.Ui_MainWindow._download_()


def _download_(self):
    notes = NotesExtract.ObtainPptNote(MainWindow.Ui_MainWindow.file_dir)
    gender_opt = MainWindow.Ui_MainWindow.ChooseSpeakerId.currentText()
    if MainWindow.Ui_MainWindow.PinyinCheck.isChecked():
        MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" "
                                                 "font-size:14pt; color:#0000cd;\""
                                                 ">正在获取备注及拼音..."
                                                 "</span></p></body></html>"))
        for i in range(0, len(notes)):
            if notes[i] == '\n':
                continue
            else:
                slide = tts.tts(notes[i], gender_opt)
                MainWindow.Ui_MainWindow.TextBrowser.append(slide[0])
                MainWindow.Ui_MainWindow.PinyinEdit.append(slide[1])
        MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                 "<html><head/><body><p><span style=\""
                                                 " font-size:14pt; color:#21ff06;\""
                                                 ">备注及拼音获取完成!请核对修改拼音!</span></p></body></html>"))
        return
    for i in range(0, len(notes)):
        if notes[i] == '\n':
            continue
        MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                 "<html><head/><body><p><span style=\" "
                                                 "font-size:14pt; color:#0000cd;\""
                                                 ">正在处理第" + str(i + 1) + "页幻灯片..."
                                                                         "</span></p></body></html>"))

        url = tts.tts(notes[i], gender_opt)
        if url is None:
            MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                                     "<html><head/><body><p><span style=\" "
                                                     "font-size:14pt; color:#ff0000;\""
                                                     ">转换出错!请重试!</span></p></body></html>"))
            return
        f = requests.get(url)
        with open(str(i + 1) + ".wav", "wb") as code:
            code.write(f.content)
    MainWindow.Ui_MainWindow.StatusLabel.setText(MainWindow.Ui_MainWindow._translate("MainWindow",
                                             "<html><head/><body><p><span style=\""
                                             " font-size:14pt; color:#21ff06;\""
                                             ">音频转换完成!</span></p></body></html>"))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = MainWindow.Ui_MainWindow.Ui_MainWindow()
    ui.setupUi(mainWindow)
    MainWindow.Ui_MainWindow.show()
    sys.exit(app.exec_())
