import numpy, wave
import matplotlib.pyplot as plt
import numpy as np
import os

global filepath
# filepath = "E:\python\python-workspace\pyqt\practice\data\demo.wav"
filepath = "demo.wav"
class GetDiagram():
    f = wave.open(filepath, 'rb')  # 调用wave模块中的open函数，打开语音文件
    params = f.getparams() # 得到语音参数
    # nchannels:音频通道数，sampwidth:每个音频样本的字节数，framerate:采样率，nframes:音频采样点数
    nchannels, sampwidth, framerate, nframes = params[:4]
    strData = f.readframes(nframes)  # 读取音频，字符串格式
    wavaData = np.fromstring(strData, dtype=np.int16)  # 得到的数据是字符串，将字符串转为int型
    wavaData = wavaData * 1.0 / max(abs(wavaData))  # wave幅值归一化
    wavaData = np.reshape(wavaData, [nframes, nchannels]).T  # .T 表示转置
    f.close()

    #绘制语谱图
    def getSpectrogram(self):
        plt.figure()
        # 绘制频谱
        plt.specgram(self.wavaData[0], Fs=self.framerate, scale_by_freq=True, sides='default')
        # plt.xlabel('Time(s)')
        # plt.ylabel('Frequency')
        plt.savefig('E:\python\python-workspace\pyqt\practice\picture/spectrogram.jpg')  # 保存绘制的图形
        plt.show()

    # 绘制时域图
    def getTimeDomainDiagram(self):
        time = np.arange(0, self.nframes) * (1.0 / self.framerate)
        time = np.reshape(time, [self.nframes, 1]).T
        plt.plot(time[0, :self.nframes], self.wavaData[0, :self.nframes], c="b")
        # plt.xlabel("time(seconds)")
        # plt.ylabel("amplitude")
        plt.savefig('E:\python\python-workspace\pyqt\practice\picture/timeDomainDiagram.jpg')  # 保存绘制的图形
        plt.show()

if __name__ == "__main__":
    GetDiagram().getSpectrogram()
    GetDiagram().getTimeDomainDiagram()
