# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:17:02 2019

@author: Leonardo
"""

import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew

#Funções

#Médias
#média das médias
def media(lista_dif):
    lista_media = []
    for i in range(len(lista_dif)):
        lista_media.append((lista_dif[i] + lista_dif_index[i])/2)
    return lista_media

#média das janelas
def mediax(lista_dif_index):
    media = sum(lista_dif_index)/len(lista_dif_index)
    return media
def mediay(lista_dif):
    media = sum(lista_dif)/len(lista_dif)
    return media

#funções para picos
def peaks(lista):    
    #distancia = frequencia amostral
    peaks, _ = find_peaks(lista, distance=fs//2)
    np.diff(peaks)    
    return peaks

def num_peaks(lista, peaks):    
    #duferença picos
    num_peaks = np.zeros(len(peaks)-2)
    for i in range(len(peaks)-2):
        num_peaks[i]=lista[peaks[i]]-lista[peaks[i+1]]
    return num_peaks

def comport(s, lista_dif, peaks):
    for i in range(len(s)-1):
        sub = abs(s[i]-s[i+1])
        lista_dif.append(sub)
    return lista_dif
        
def comport_index(s, lista_dif_index, peaks):
    for i in range(len(s)-1):
        sub_index = abs(peaks[i]-peaks[i+1])
        lista_dif_index.append(sub_index)
    return lista_dif_index

def plot_comport(lista, peaks):
    #plot de comportamento dos picos
    s = lista[peaks]
    lista_dif = []
    lista_dif_index = []
    return comport(s, lista_dif, lista_dif_index, peaks)   



# REFERENCIA
# https://media.readthedocs.org/pdf/python-heart-rate-analysis-toolkit/latest/python-heart-rate-analysis-toolkit.pdf
# x = electrocardiogram()#[2000:4000]
data = pd.read_csv('lista2.txt')
data2 = pd.read_csv('lista3.txt')
fs = 128
J = 300 #5x60
jfs = J*fs

for w in range(0,1):
    ecg = np.load(data['nome'][w])
    ecg2 = np.load(data2['nome'][w])
    #janelamento
    #precisa ser feito a partir do período de cada janela = 5 min x frequencia amostral = 128hz
    #sendo T o período total da amostra
    T = len(ecg)
    T2 = len(ecg2)    
    aux = 120000
    aux2 = aux + jfs
    lista_media_x = []
    lista_media_y = []
    k_list = []
    skew_list = []
    
    
    while(aux2<=len(ecg)):
                
        x = ecg[aux:aux2]
        #k = ecg2[aux:aux]
        
        #limiar
        #aux = np.repeat(3*np.std(x), len(x))
        
        peaks1 = peaks(x)       
        s = x[peaks1]
        numero1 = num_peaks(x, peaks1)
        lista_dif = []
        comport1 = comport(s, lista_dif, peaks1)
        lista_dif_index = []
        comport_index1 = comport_index(s, lista_dif_index, peaks1)
        lista_media1 = media(lista_dif)    
        #variancias
        variancia1 = pd.Series(lista_media1).var()    
        #curtose    
        k = kurtosis(lista_media1)
        k_list.append(k)
        #coeficiente de assimetria    
        skew_val = skew(lista_media1)
        skew_list.append(skew_val)
        
        aux += jfs
        aux2 += jfs

    
    
    plt.plot(k_list,"o")
    plt.plot(skew_list, "o")
    
   # plt.plot(k2,"o")
    plt.show()

    
    
    