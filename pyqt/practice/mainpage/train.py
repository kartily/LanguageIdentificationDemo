import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
import pandas as pd
from tqdm import tqdm
from torchvision.transforms import transforms
from torchvision.models.resnet import Bottleneck, BasicBlock
from practice.mainpage.dataset import *
from practice.mainpage.model import *
num_workers = 16
# %% network
net =xvecTDNN(numSpkrs=14,p_dropout=0)  #语种个数--14 -- 模型（model.py）
device = torch.device('cpu')
# 数据处理
class CopeData():
    def __init__(self,filepath):
        self.feature = np.load(filepath)   #获取特征数据
        self.max_width = 6900
    # 处理数据
    def transform(self):
        # 1.获取输入 -- 设置最大宽度为6900
        buckets = [i * 100 for i in range(1, int(self.max_width / 100) + 1)]
        # print("feature--",self.feature.shape)  #feature-- (69, 398)
        rsize = self.feature.shape[1]
        for width in buckets:
            if width <= self.feature.shape[1]:
                rsize = width
            else:
                break
        rstart = round((self.feature.shape[1] - rsize) / 2 )
        input_feature = self.feature[:,rstart:rstart+rsize]

        # 2.标准化
        input_feature = np.array([(v - np.mean(v)) / max(np.std(v), 1e-8) for v in input_feature])

        # 3.数据填充 -- 不足6900的补0，使长度达到6900
        padding_width = self.max_width - input_feature.shape[1]  # 填充长度=最大长度-数据自身长度
        if input_feature.shape[1] < self.max_width:  # 不够--需要填充
            zeros = np.zeros((input_feature.shape[0], padding_width))  # 返回来一个给定形状和类型的用0填充的数组
            input_feature = np.concatenate((input_feature, zeros), axis=1)  # 数组拼接（对应行数组进行拼接）
        # 构建一个数组，形状-(frames_feature.shape[0], 1)，元素-padding_width
        padding_width_array = np.full((input_feature.shape[0], 1),padding_width)
        # 数组拼接（对应行数组进行拼接）
        input_feature = np.concatenate((input_feature, padding_width_array), axis=1)

        # 4.转化为张量
        F,T = input_feature.shape
        input_feature = input_feature.reshape(1,F,T)
        input_feature = input_feature.astype(np.float32)
        # print("torch.from_numpy(input_feature)--",torch.from_numpy(input_feature).shape)  # torch.from_numpy(input_feature)-- torch.Size([69, 6901])
        return torch.from_numpy(input_feature)

# 加载模型--进行语种识别
class GetLanguage():
    def __init__(self,filepath):
        self.filepath = filepath
    def test(self):
        pretrained_dict = torch.load('epoch_30',map_location='cpu')  # 加载模型
        net.load_state_dict(pretrained_dict,strict=False) #数据加载到模型中
        net.eval()
        data = CopeData(self.filepath).transform()
        # data = data.to(c.device)
        score = net(data,'test',1e-8)
        # print("sorce--",score.shape)  # sorce-- torch.Size([1, 14])
        # print("sorce--", score)
        # print("sorce--", score.detach().numpy().shape)  # sorce-- (1, 14)
        # print("sorce--", score.detach().numpy()[0])
        s = score.detach().numpy()[0]
        # print(len(s))  # 14
        language = ['arabic','bengali','chinese','english','farsi','german','hindustani',
                    'japanese','korean','russian','spanish','tamil','thai','vietnamese']
        for i in range(13):
            for j in range(13-i):
                if s[j]<s[j+1]:
                    s[j],s[j+1] = s[j+1],s[j]
                    language[j],language[j+1] = language[j+1],language[j]

        print(language)
        # print(s)
        return language



if __name__ == '__main__':
    # filepath = 'demo.npy'
    filepath = '../data/thai_train_lre07_tr_tha_024_b.npy'
    # data = CopeData(filepath).transform()
    # print("data--",data.shape)  # data-- torch.Size([69, 6901])
    data = GetLanguage(filepath).test()
    print(data)