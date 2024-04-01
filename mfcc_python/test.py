import pandas as pd
import numpy as np
import random

num = np.dtype({
    'names':['train','enroll','test'],
    'formats':['f','f','f']
})
num.train = 100
print('train--%f' %num.train)
