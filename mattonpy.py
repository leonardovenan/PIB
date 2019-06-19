import numpy as np
import pandas as pd 
import scipy.io as sio

mtn = lambda arq:sio.loadmat(arq)

l = pd.read_csv('C:/Users/Leonardo/Desktop/ecg/Nao Saudavel/lista.txt')
c = 'C:/Users/Leonardo/Desktop/ecg/Nao Saudavel/'

for i in range(1,len(l)):
    arq = mtn(c + l['nome'][i])
    ecg = arq['val'][0]
    np.save('ecg_'+str(i)+'.npy',ecg)