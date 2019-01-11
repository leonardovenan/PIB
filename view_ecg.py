# Visualição de ECG

import numpy as np
import pandas as pd 
import scipy.io as sio 
import matplotlib.pyplot as plt
import mne

# .mat para numpy.array
mtn = lambda arq:sio.loadmat(arq)

# Plotando com MNE
# def view(data):
#     info = mne.create_info(ch_names=['CH1','CH2'],sfreq=128,
#     ch_types=['ecg','ecg'])
#     raw = mne.io.RawArray(data,info)
#     raw.plot(n_channels=2,scalings='auto',show=True,block=True)
"""
def view(data):
    info = mne.create_info(ch_names=['CH1'],sfreq=128,
    ch_types=['ecg'])
    raw = mne.io.RawArray(data,info)
    raw.plot(n_channels=1,scalings='auto',show=True,block=True)
"""
# Carregando sinal
cw = 'MIT_BIH_Atrial_Fibrillation_Database/'
cn = 'MIT_BIH_Normal_Sinus_Rhythm/'

w = pd.read_csv('w.txt')
n = pd.read_csv('n.txt')

arq = mtn(cw + w['name'][0])
ecg = arq['val']

print (ecg.shape)

x = ecg[0]
print (x)



lista_indice = []
lista_valor = []
lista_picos = []
lista_index_picos = []

for y in range(len(x[:1000])):
    if x[y] > 70:
        lista_indice.append(y)
        lista_valor.append(x[y])
        if (x[y]>x[y-1] and x[y] > x[y+1]):
            lista_picos.append(x[y])
            lista_index_picos.append(y)
            
plt.plot(x[:1000]) 
plt.plot(lista_index_picos, lista_picos, linestyle=' ', color='r', marker='s', 
         linewidth=3.0)




    



