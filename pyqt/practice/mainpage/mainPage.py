import numpy, wave
import matplotlib.pyplot as plt
import numpy as np
import os
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
import pyaudio
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QPalette, QIcon, QPixmap
import sys
import qtawesome
from PyQt5.QtWidgets import *
from practice.mainpage.getMFCC import *
from practice.mainpage.train import *

global voice_btn_clicked
global filepath
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        # 主窗口大小
        self.setWindowTitle("语种识别")
        # self.setWindowOpacity(0.9)  # 窗口透明度
        self.setFixedSize(1000, 600)

        #个人中心
        self.user_hub = QtWidgets.QPushButton(self)
        self.user_hub.setGeometry(QtCore.QRect(900, 20, 40, 40))
        self.user_hub.setObjectName("user_hub")
        # 标题
        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setGeometry(QtCore.QRect(500, 60, 400, 70))
        self.title_label.setObjectName("title_label")

        #文本框
        self.text_label = QtWidgets.QLabel(self)
        self.text_label.setGeometry(QtCore.QRect(500, 150, 400, 200))
        self.text_label.setObjectName("text_label")

        # 音频文件位置文本框
        self.filepath_label = QtWidgets.QLabel(self)
        self.filepath_label.setGeometry(QtCore.QRect(500, 520, 500, 50))
        self.filepath_label.setObjectName("filepath_label")
        self.filepath_label.setWordWrap(True)

        #输入语音按钮
        self.thread = MyThread()  # 创建一个线程
        self.thread.sec_changed_signal.connect(self.get_flames)  # 线程发过来的信号挂接到槽：updat
        self.voice_button = QtWidgets.QPushButton(self)
        self.voice_button.setGeometry(QtCore.QRect(500, 430, 101, 71))
        self.voice_button.setObjectName("voice_button")

        # 定义按钮点击事件
        global voice_btn_clicked   #按钮初始化 0-停止录音 1-开始录音
        voice_btn_clicked=0
        self.voice_button.clicked.connect(self.voiceButtonClicked)

        #打开文件按钮
        self.file_button = QtWidgets.QPushButton(self)
        self.file_button.setGeometry(QtCore.QRect(650, 430, 101, 71))
        self.file_button.setObjectName("file_Button")
        self.file_button.clicked.connect(self.fileButtonClicked)

        #开始识别按钮
        self.recognition_button = QtWidgets.QPushButton(self)
        self.recognition_button.setGeometry(QtCore.QRect(800, 430, 101, 71))
        self.recognition_button.setObjectName("recognition_button")
        self.recognition_button.clicked.connect(self.selfrecognitionButtonClicked)

        #---------------------------------------------------------------------------
        #语谱图与时域图
        #语谱图 spectrogram
        self.spectrogram_label = QtWidgets.QLabel(self)
        self.spectrogram_label.setGeometry(QtCore.QRect(30, 50, 400, 50))
        self.spectrogram_label.setObjectName("spectrogram_label")

        self.getSpectrogram_label = QtWidgets.QLabel(self)
        self.getSpectrogram_label.setGeometry(QtCore.QRect(30, 100, 400, 200))
        self.getSpectrogram_label.setFixedSize(400, 200)
        self.getSpectrogram_label.setObjectName("getSpectrogram_label")

        #时域图timeDomainDiagram
        self.timeDomainDiagram_label = QtWidgets.QLabel(self)
        self.timeDomainDiagram_label.setGeometry(QtCore.QRect(30, 300, 400, 50))
        self.timeDomainDiagram_label.setObjectName("timeDomainDiagram_label")

        self.getTimeDomainDiagram_label = QtWidgets.QLabel(self)
        self.getTimeDomainDiagram_label.setGeometry(QtCore.QRect(30, 350, 400, 200))
        self.getTimeDomainDiagram_label.setFixedSize(400, 200)
        self.getTimeDomainDiagram_label.setObjectName("getTimeDomainDiagram_label")

        # 美化操作
        self.retranslateUi()  # 美化主体
        self.retranslateControl()  # 美化控件

    # 美化主体
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.user_hub.setText(_translate("MainWindow", ""))
        self.voice_button.setText(_translate("MainWindow", ""))
        self.title_label.setText(_translate("MainWindow", "语种识别"))
        self.text_label.setText("点击下面的按钮开始录制音频\n"
                                "再次点击停止录音开始识别\n"
                                "或从文件夹中选择要识别的语音文件")
        self.spectrogram_label.setText("getSpectrogram")
        self.timeDomainDiagram_label.setText("getTimeDomainDiagram")
        pe = QPalette()
        self.setAutoFillBackground(True)
        # pe.setColor(QPalette.Window,Qt.lightGray)  #设置背景色
        self.setPalette(pe)

        # 设置标题和图标
        self.setWindowTitle("语音识别")
        self.setWindowIcon(QIcon('Amg.jpg'))  # 设置图标
        spin_icon = qtawesome.icon('fa5s.microphone-alt', color='black')
        # self.pushButton.setIcon(spin_icon)#设置图标
        self.setWindowIcon(spin_icon)

    # 美化控件
    def retranslateControl(self):
        #美化label
        self.title_label.setStyleSheet('''QLabel{color:black;
                            font-size:40px;
                            font-family:Roman times;}''')
        self.text_label.setStyleSheet('''QLabel{color:darkGray;
                            background:white;
                            border:2px solid #000000;
                            border-radius:45px;
                            font-size:14pt;
                            font-weight:400;
                            font-family: Roman times;} ''')
        self.filepath_label.setStyleSheet('''QLabel{font-size:14pt;
                           font-weight:400;
                           font-family: Roman times;} ''')
        # 时域图与语谱图
        self.spectrogram_label.setStyleSheet('''QLabel{color:black;
                                font-size:25px;
                                font-family:Roman times;}''')
        self.timeDomainDiagram_label.setStyleSheet('''QLabel{color:black;
                                font-size:25px;
                                font-family:Roman times;}''')
        self.getSpectrogram_label.setStyleSheet('''QLabel{color:black;border:2px solid #000000;}''')
        self.getTimeDomainDiagram_label.setStyleSheet('''QLabel{color:black;border:2px solid #000000;}''')
        #label字体居中显示
        self.text_label.setAlignment(Qt.AlignCenter)
        self.title_label.setAlignment(Qt.AlignCenter)

        # 美化按钮
        # 录音按钮
        spin_icon = qtawesome.icon('fa5s.microphone-alt', color='black')
        self.voice_button.setIcon(spin_icon)#设置图标
        self.voice_button.setIconSize(QtCore.QSize(50,50))
        self.voice_button.setStyleSheet('''QPushButton{color:black;
                        border:2px solid #000000;
                        border-radius:35px;}
                QPushButton:hover{color:white;
                        border:2px solid #F3F3F5;
                        border-radius:35px;
                        background:darkGray;}''')
        #选择文件按钮
        file_icon = qtawesome.icon('fa5s.folder',color='black')
        self.file_button.setIcon(file_icon)
        self.file_button.setIconSize(QtCore.QSize(50, 50))
        self.file_button.setStyleSheet('''QPushButton{color:black;
                                    border:2px solid #000000;
                                    border-radius:35px;}
                            QPushButton:hover{color:white;
                                border:2px solid #F3F3F5;
                                border-radius:35px;
                                background:darkGray;}''')
        # 语音识别按钮
        self.recognition_button.setText("开始识别")
        self.recognition_button.setIconSize(QtCore.QSize(50, 50))
        self.recognition_button.setStyleSheet('''QPushButton{color:black;
                                                font-size:12pt;
                                                border:2px solid #000000;
                                                border-radius:35px;}
                                        QPushButton:hover{color:white;
                                                border:2px solid #F3F3F5;
                                                border-radius:35px;
                                                background:darkGray;}''')
        #用户中心
        user_icon = qtawesome.icon('fa5s.address-card',color='black')
        self.user_hub.setIcon(user_icon)
        self.user_hub.setIconSize(QtCore.QSize(40, 40))
        self.user_hub.setStyleSheet('''QPushButton{border:none;}
                                    QPushButton:hover{color:white;
                                            border:2px solid #F3F3F5;
                                            border-radius:35px;
                                            background:darkGray;}''')

    # 识别结果输出样式
    def dist_textlabel_ui(self):
        self.text_label.setStyleSheet('''QLabel{
                                    background:white;
                                    border:2px solid #000000;
                                    border-radius:45px;
                                    font-size:18pt;
                                    font-weight:400;
                                    font-family: Roman times;} ''')

    # 进行槽函数的连接 能够获取到录音
    def get_flames(self,flames):
        self.flames=flames

    #点击输入语音按钮
    def voiceButtonClicked(self):
        # print("点击录音")
        global voice_btn_clicked
        voice_btn_clicked += 1
        # print("clicked--",voice_btn_clicked%2)
        if voice_btn_clicked%2 == 1:  # 1-开始录音
            self.thread.start()  #开启线程，开始录音
            # QMessageBox.information(self, '提示', '开始录音！')
            # print("开始录音！！！")
        else:  # 0- 停止录音
            self.saveVoice()
            # QMessageBox.information(self, '提示', '停止录音！')
            # print("结束录音！！！")

    #保存录音
    def saveVoice(self):
        print("保存录音")
        CHUNK = 1024  # 每个
        FORMAT = pyaudio.paInt16  # 采样位数#一帧占两字节
        CHANNELS = 1  # 声道
        RATE = 44100  # 采样频率
        self.thread.terminate() #结束录音进程

        # 弹出标准对话框，获取录音保存名
        filename,ok = QInputDialog.getText(self,'保存文件名','文件名：')
        if ok:
            print("filename--",filename)
            p = pyaudio.PyAudio()
            # wav_file = wave.open(f"../data/{filename}.wav",'wb')  #打开文件进行保存
            global filepath
            filepath = f"F:\python\PythonWorkspace\lid-demo\pyqt\practice\data\{filename}.wav"
            wav_file = wave.open(filepath, 'wb')  # 打开文件进行保存
            print("filepath--",filepath)
            wav_file.setnchannels(CHANNELS)
            wav_file.setsampwidth(p.get_sample_size(FORMAT))
            wav_file.setframerate(RATE)
            wav_file.writeframes(b''.join(self.flames))  #写入数据
            # print(wav_file.getfp())
            wav_file.close()
            self.filepath_label.setText(filepath)

    #点击选择文件
    def fileButtonClicked(self):
        # fileName, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
        #                                                   "Voice Files (*.wav);;Voice1 Files (*.mp3)")  # 设置文件扩展名过滤,注意用双分号间隔
        # print(fileName) #E:/python/python-workspace/pyqt/practice/data/demo.wav(文件路径)
        global filepath
        filepath, filetype = QFileDialog.getOpenFileName(self, "选取文件", "./",
                                                         "Voice Files (*.wav);;Voice1 Files (*.mp3)")  # 设置文件扩展名过滤,注意用双分号间隔
        self.filepath_label.setText(filepath)
        print(filepath)  # E:/python/python-workspace/pyqt/practice/data/demo.wav(文件路径)

    #点击开始识别
    def selfrecognitionButtonClicked(self):
        print("start")
        #获得语谱图  E:\python\python-workspace\pyqt\practice\picture\spectrogram.jpg
        self.getSpectrogram()
        self.getSpectrogram_label.setPixmap(QPixmap("F:\python\PythonWorkspace\lid-demo\pyqt\practice\picture\spectrogram.jpg"))
        self.getSpectrogram_label.setScaledContents(True) #图片自适应大小
        # print("getSpectrogram")
        #获得时域图  E:\python\python-workspace\pyqt\practice\picture/timeDomainDiagram.jpg
        self.getTimeDomainDiagram()
        self.getTimeDomainDiagram_label.setPixmap(QPixmap("F:\python\PythonWorkspace\lid-demo\pyqt\practice\picture/timeDomainDiagram.jpg"))
        self.getTimeDomainDiagram_label.setScaledContents(True)  # 图片自适应大小
        # print("getTimeDomainDiagram")
        #语种识别
        self.languageIdentify()
        print("start--")

    # 绘制语谱图
    def getSpectrogram(self):
        f = wave.open(filepath, 'rb')  # 调用wave模块中的open函数，打开语音文件
        params = f.getparams()  # 得到语音参数
        # nchannels:音频通道数，sampwidth:每个音频样本的字节数，framerate:采样率，nframes:音频采样点数
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)  # 读取音频，字符串格式
        wavaData = np.fromstring(strData, dtype=np.int16)  # 得到的数据是字符串，将字符串转为int型
        wavaData = wavaData * 1.0 / max(abs(wavaData))  # wave幅值归一化
        wavaData = np.reshape(wavaData, [nframes, nchannels]).T  # .T 表示转置
        f.close()

        plt.figure()
        # 绘制频谱
        plt.specgram(wavaData[0], Fs=framerate, scale_by_freq=True, sides='default')
        # plt.xlabel('Time(s)')
        # plt.ylabel('Frequency')
        plt.savefig('F:\python\PythonWorkspace\lid-demo\pyqt\practice\picture\spectrogram.jpg')  # 保存绘制的图形
        plt.show()

    # 绘制时域图
    def getTimeDomainDiagram(self):
        f = wave.open(filepath, 'rb')  # 调用wave模块中的open函数，打开语音文件
        params = f.getparams()  # 得到语音参数
        # nchannels:音频通道数，sampwidth:每个音频样本的字节数，framerate:采样率，nframes:音频采样点数
        nchannels, sampwidth, framerate, nframes = params[:4]
        strData = f.readframes(nframes)  # 读取音频，字符串格式
        wavaData = np.fromstring(strData, dtype=np.int16)  # 得到的数据是字符串，将字符串转为int型
        wavaData = wavaData * 1.0 / max(abs(wavaData))  # wave幅值归一化
        wavaData = np.reshape(wavaData, [nframes, nchannels]).T  # .T 表示转置
        f.close()

        time = np.arange(0, nframes) * (1.0 / framerate)
        time = np.reshape(time, [nframes, 1]).T
        plt.plot(time[0, :nframes], wavaData[0, :nframes], c="b")
        # plt.xlabel("time(seconds)")
        # plt.ylabel("amplitude")
        plt.savefig("F:\python\PythonWorkspace\lid-demo\pyqt\practice\picture/timeDomainDiagram.jpg")  # 保存绘制的图形
        plt.show()

    #语种识别
    def languageIdentify(self):
        # print("filepath--",filepath)
        feature =GetMfcc(filepath).get_mfcc()
        print("feature--",feature.shape)  #feature-- (69, 398)
        np.save("demo.npy", feature)
        npy_path = 'demo.npy'
        language = GetLanguage(npy_path).test()
        # print(language)
        self.text_label.setText('识别结果前三种可能：'+'\n'+language[0]+'\n'+language[1]+'\n'+language[2])
        self.dist_textlabel_ui()

#多线程进行录音
class MyThread(QThread):
    sec_changed_signal = pyqtSignal(list)  # 信号类型：int
    def __init__(self, parent=None):
        super().__init__(parent)
    def run(self):
        print("开始录音")
        CHUNK = 1024  # 每个
        FORMAT = pyaudio.paInt16  # 采样位数#一帧占两字节
        CHANNELS = 1  # 声道
        RATE = 44100  # 采样频率
        p = pyaudio.PyAudio() #实例化对象
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)  # 打开流，传入响应参数
        frames = []
        while True:  # 还在录音
            data = stream.read(CHUNK)
            frames.append(data)  #录音
            self.sec_changed_signal.emit(frames)


if __name__ == '__main__':
    page = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(page.exec_())