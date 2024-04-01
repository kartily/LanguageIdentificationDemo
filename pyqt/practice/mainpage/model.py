import torch.nn as nn
import math
import torch
import constants as c
import torch.nn.functional as F
# from sklearn.preprocessing import minmax_scale
class xvecTDNN(nn.Module):

    def __init__(self, numSpkrs, p_dropout): #带Dropout的网络可以防止出现过拟合。设置Dropout时，torch.nn.Dropout(0.5), 这里的 0.5 是指该层（layer）的神经元在每次迭代训练时会随机有 50% 的可能性被丢弃（失活），不参与训练，一般多神经元的 layer 设置随机失活的可能性比神经元少的高。

        super(xvecTDNN, self).__init__()
        self.tdnn1 = nn.Conv1d(in_channels=69, out_channels=512, kernel_size=5, dilation=1)  #一个卷积核包含图像的一种特征，做卷积运算实际上说白了就是在计算卷积核上面的特征和图像上面特征的相似度，相似度越高，越认为这图就是拥有此特征。
        self.bn_tdnn1 = nn.BatchNorm1d(512, momentum=0.1, affine=False) #Batch Normal1d是在隐藏层中使用，可以将数据从偏移状态拉回到正态分布。
        self.dropout_tdnn1 = nn.Dropout(p=p_dropout)#随机将输入张量中部分元素设置为0。对于每次前向调用，被置为0的元素都是随机的

        self.tdnn2 = nn.Conv1d(in_channels=512, out_channels=512, kernel_size=5, dilation=2)#dilation卷积核内部各点的间距，整数或者元组
        self.bn_tdnn2 = nn.BatchNorm1d(512, momentum=0.1, affine=False)
        self.dropout_tdnn2 = nn.Dropout(p=p_dropout)

        self.tdnn3 = nn.Conv1d(in_channels=512, out_channels=512, kernel_size=7, dilation=3)
        self.bn_tdnn3 = nn.BatchNorm1d(512, momentum=0.1, affine=False)
        self.dropout_tdnn3 = nn.Dropout(p=p_dropout)

        self.tdnn4 = nn.Conv1d(in_channels=512, out_channels=512, kernel_size=1, dilation=1)
        self.bn_tdnn4 = nn.BatchNorm1d(512, momentum=0.1, affine=False)
        self.dropout_tdnn4 = nn.Dropout(p=p_dropout)

        self.tdnn5 = nn.Conv1d(in_channels=512, out_channels=1500, kernel_size=1, dilation=1)
        self.bn_tdnn5 = nn.BatchNorm1d(1500, momentum=0.1, affine=False)
        self.dropout_tdnn5 = nn.Dropout(p=p_dropout)

        self.fc1 = nn.Linear(3000,512)
        self.bn_fc1 = nn.BatchNorm1d(512, momentum=0.1, affine=False)
        self.dropout_fc1 = nn.Dropout(p=p_dropout)

        self.fc2 = nn.Linear(512,512)
        self.bn_fc2 = nn.BatchNorm1d(512, momentum=0.1, affine=False)
        self.dropout_fc2 = nn.Dropout(p=p_dropout)

        self.fc3 = nn.Linear(512,numSpkrs)
    def forward_once(self, x, eps):
         # Note: x must be (batch_size, feat_dim, chunk_len)

        x = self.dropout_tdnn1(self.bn_tdnn1(F.relu(self.tdnn1(x))))
        x = self.dropout_tdnn2(self.bn_tdnn2(F.relu(self.tdnn2(x))))
        x = self.dropout_tdnn3(self.bn_tdnn3(F.relu(self.tdnn3(x))))
        x = self.dropout_tdnn4(self.bn_tdnn4(F.relu(self.tdnn4(x))))
        x = self.dropout_tdnn5(self.bn_tdnn5(F.relu(self.tdnn5(x))))

        if self.training:
            #x = x + torch.randn(x.size()).cuda()*eps #torch.randn(*size) : 服从正太分布初始化，返回一个符合均值为0，方差为1的正态分布（标准正态分布）中填充随机数的张量  使用.cuda将计算或者数据从CPU移动至GPU， 
            x = x + torch.randn(x.size()).cuda()*eps
        stats = torch.cat((x.mean(dim=2), x.std(dim=2)), dim=1) #torch.cat((tensor1,tensor2), dim) 将两个tensor连接起来，当为二维张量时，用torch.cat拼接的时候就有两种拼接方式：按行拼接和按列拼接。即所谓的维数0和维数1. 
        x = self.dropout_fc1(self.bn_fc1(F.relu(self.fc1(stats)))) #tensor按照均值mean和标准差std进行归一化
        x = self.dropout_fc2(self.bn_fc2(F.relu(self.fc2(x))))  #倒数第二层 -- 得到512维向量
        return x


    def forward(self, x, phrase,eps):
        if phrase == 'triplet':  # 训练
            x = self.forward_once(x,eps)
        elif phrase == 'evaluation':  # 测试
            #_padding_width = x[0, 0, 0, -1]
            _padding_width = x[0, 0, -1]
            x = x[:, :, :-1 - int(_padding_width.item())]
            x = self.forward_once(x,eps)
        elif phrase == 'test':  # 语种识别
            #_padding_width = x[0, 0, 0, -1]
            # print("x--", x.shape)  # x-- torch.Size([69, 6901])
            _padding_width = x[0,0,-1]
            x = x[:, :, :-1 - int(_padding_width.item())]
            x = self.forward_once(x,eps)
            x = self.fc3(x)  #预测语种 -- 14个数 -- 每种语种的可能性
        elif phrase == 'pretrain':  # 预训练
            x = self.forward_once(x,eps)
            x = self.fc3(x)
        else:
            raise ValueError('phase wrong!')
        return x

class VGGVox1(nn.Module):

    def __init__(self, num_classes=1211, emb_dim=1024):
        super(VGGVox1, self).__init__()
        self.num_classes = num_classes
        self.emb_dim = emb_dim
        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=96, kernel_size=7, stride=2, padding=1),
            nn.BatchNorm2d(num_features=96),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )
        self.conv2 = nn.Sequential(
            nn.Conv2d(in_channels=96, out_channels=256, kernel_size=5, stride=2, padding=1),
            nn.BatchNorm2d(num_features=256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=3, stride=2)
        )
        self.conv3 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=384, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_features=384),
            nn.ReLU(inplace=True)
        )
        self.conv4 = nn.Sequential(
            nn.Conv2d(in_channels=384, out_channels=256, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_features=256),
            nn.ReLU(inplace=True)
        )
        self.conv5 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=256, kernel_size=3, padding=1),
            nn.BatchNorm2d(num_features=256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=(5, 3), stride=(3, 2))
        )
        self.fc6 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=4096, kernel_size=(4, 1)),
            nn.BatchNorm2d(num_features=4096),
            nn.ReLU(inplace=True)
        )
        self.fc7 = nn.Linear(in_features=4096, out_features=self.emb_dim) #in_features指的是输入的二维张量的大小，即输入的[batch_size, size]中的size。out_features指的是输出的二维张量的大小，即输出的二维张量的形状为[batch_size，output_size]，当然，它也代表了该全连接层的神经元个数。
        self.fc8 = nn.Linear(in_features=self.emb_dim, out_features=self.num_classes)

        # nn.init.xavier_uniform_(self.fc8.weight)

    def forward_once(self, x):
        out = self.conv1(x)
        out = self.conv2(out)
        out = self.conv3(out)
        out = self.conv4(out)
        out = self.conv5(out)
        out = self.fc6(out)
        # global average pooling layer
        _, _, _, width = out.size()
        self.apool6 = nn.AvgPool2d(kernel_size=(1, width))
        out = self.apool6(out)
        out = out.view(out.size(0), -1)
        out = self.fc7(out)
        return out

    def forward(self, x, phase):
        if phase == 'evaluation':
            _padding_width = x[0, 0, 0, -1]
            out = x[:, :, :, :-1 - int(_padding_width.item())]
            out = self.forward_once(out)
            # out = F.normalize(out, p=2, dim=1)

        elif phase == 'triplet':
            out = self.forward_once(x)
            out = F.normalize(out, p=2, dim=1)

        elif phase == 'pretrain':
            out = self.forward_once(x)
            out = self.fc8(out)
        else:
            raise ValueError('phase wrong!')
        return out


class OnlineTripletLoss(nn.Module):
        #     """
        # Online Triplets loss
        # Takes a batch of embeddings and corresponding labels.
        # Triplets are generated using triplet_selector object that take embeddings and targets and return indices of
        # triplets

        # Reference: https://github.com/adambielski/siamese-triplet
        #     """

    def __init__(self, margin, triplet_selector):
        super(OnlineTripletLoss, self).__init__()
        self.margin = margin
        self.triplet_selector = triplet_selector

    def forward(self, embeddings, target):
        triplets = self.triplet_selector.get_triplets(
            embeddings.detach(), target)

        if embeddings.is_cuda:
            triplets = triplets.to(c.device)
        
        
        # l2 distance
        ap_distances = (embeddings[triplets[:, 0]] - embeddings[triplets[:, 1]]).pow(2).sum(1).pow(.5)
        an_distances = (embeddings[triplets[:, 0]] - embeddings[triplets[:, 2]]).pow(2).sum(1).pow(.5)
        # losses = torch.mean(ap_distances)-torch.log(torch.mean(torch.exp(an_distances)))
        losses = F.relu(ap_distances - an_distances + self.margin)

        '''
        # cosine similarity
        cos = torch.nn.CosineSimilarity(dim=1)
        ap_similarity = cos(embeddings[triplets[:, 0]], embeddings[triplets[:, 1]])
        an_similarity = cos(embeddings[triplets[:, 0]], embeddings[triplets[:, 2]])
        # losses = -(torch.mean(ap_similarity)-torch.log(torch.mean(torch.exp(an_similarity-1))))
        #losses = torch.mean(torch.exp(an_similarity-1)) - torch.mean(ap_similarity)
        losses = F.relu(an_similarity - ap_similarity + self.margin)
        '''
        # ap_similarity = torch.sigmoid(ap_similarity)
        # an_similarity = torch.sigmoid(an_similarity)
        # losses = (1 - an_similarity).log().mean() - ap_similarity.log().mean()

        return losses.mean(), len(triplets), ap_distances.mean(), an_distances.mean()
        #return losses.mean(), len(triplets), ap_similarity.mean(), an_similarity.mean()

