# 注意事项 #
- 本系统的语种识别模型已提前训练好（practice/mainpage/epoch_30）
	- 使用olr2020-task1数据集，提取69维mfcc特征
	- 训练模型采用x-vector模型，迭代30轮得到epoch_30
- practice/mainpage/mainPage.py下所有的文件存取路径都写的绝对路径（需要改）
- 运行环境：最好使用pyhon3.7
- mfcc_python文件夹无用
- 启动页面：practice/loginandregister/login.py
