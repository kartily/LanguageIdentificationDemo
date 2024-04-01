from python_speech_features import *
import numpy as np
import scipy.io.wavfile
from matplotlib import pyplot as plt
import scipy.io.wavfile as wav
class GetMfcc():
    def __init__(self,filepath):
        self.filename = filepath
    def get_mfcc(self):
        (rate,sig) = wav.read(self.filename) #读取wav文件（rate是wav文件的采样率，sig是wav文件的内容）
        # print("sig--",sig.shape)
        amfcc = mfcc(sig,samplerate=rate,numcep=23)   # (23, 398) (特征维度,帧数)
        # print("amfcc--", amfcc.shape)  # amfcc-- (398, 23)
        d_mfcc_feat = delta(amfcc, 1)  #一阶差分
        # print("d_mfcc_feat--",d_mfcc_feat.shape)  # d_mfcc_feat-- (398, 23)
        d_mfcc_feat2 = delta(amfcc, 2) #二阶差分
        # print("d_mfcc_feat2--", d_mfcc_feat2.shape)  # d_mfcc_feat2-- (398, 23)
        feature = np.hstack((amfcc, d_mfcc_feat, d_mfcc_feat2)) #组合
        # print("feature--",feature.shape)  #feature-- (398, 69)
        feature = feature.T  #转置
        # print("feature--", feature.shape)  # feature-- (69, 398)
        return feature


if __name__ == '__main__':
    filename = "demo.wav"
    feature = GetMfcc(filename).get_mfcc()
    np.save("demo.npy", feature)

