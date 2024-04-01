import torch
from torch.utils.data import Dataset, DataLoader
import os
import pandas as pd
import numpy as np


# 测试集
class VerificationDatasetTest1_(Dataset):
    # Full length utterances are used in testing  测试中使用完整长度的话语
    # Original voxceleb1 test set  原始voxceleb1测试集
    def __init__(self, transform=None):
        super(VerificationDatasetTest1_, self).__init__()
        self.transform = transform

    def __getitem__(self, item):
        audio_path = os.path.join('demo.npy')
        feature = np.load(audio_path)  # 读取npy文件
        # transforms
        if self.transform:
            feature = self.transform(feature)
        return feature
    def __len__(self):
        return len(self.dataset)


# ***测试截断输入??测试集
class TestTruncatedInput(object):
    # Reference: https://github.com/a-nagrani/VGGVox/blob/master/test_getinput.m

    def __init__(self, max_width=6900):
        super(TestTruncatedInput, self).__init__()
        # self.buckets = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
        self.buckets = [i * 100 for i in range(1, int(max_width / 100) + 1)]

    def __call__(self, frames_feature):
        rsize = frames_feature.shape[1]
        for width in self.buckets:
            if width <= frames_feature.shape[1]:
                rsize = width
            else:
                break
        rstart = round((frames_feature.shape[1] - rsize) / 2)
        input_feature = frames_feature[:, rstart: rstart + rsize]

        return input_feature


# **数据集填充-0  测试集
class zero_padding_test(object):

    def __init__(self, max_width=1000):
        super(zero_padding_test, self).__init__()
        self.max_width = max_width

    def __call__(self, frames_feature):
        padding_width = self.max_width - frames_feature.shape[1]  # 填充长度=最大长度-数据自身长度
        if frames_feature.shape[1] < self.max_width:  # 不够--需要填充
            zeros = np.zeros((frames_feature.shape[0], padding_width))  # 返回来一个给定形状和类型的用0填充的数组
            frames_feature = np.concatenate((frames_feature, zeros), axis=1)  # 数组拼接（对应行数组进行拼接）
        padding_width_array = np.full((frames_feature.shape[0], 1),
                                      padding_width)  # 构建一个数组，形状-(frames_feature.shape[0], 1)，元素-padding_width
        frames_feature = np.concatenate((frames_feature, padding_width_array), axis=1)  # 数组拼接（对应行数组进行拼接）
        return frames_feature


# **标准化 测试集
class normalize_frames(object):
    def __call__(self, m, epsilon=1e-8):
        return np.array([(v - np.mean(v)) / max(np.std(v), epsilon) for v in m])


# **测试集--转换为张量
class ToTensor_test(object):
    def __call__(self, spec):
        F, T = spec.shape
        # Now specs are of size (freq, time) and 2D but has to be 3D (channel dim)
        spec = spec.reshape(F, T)
        spec = spec.astype(np.float32)
        return torch.from_numpy(spec)
