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
def media(lista_dif, lista_dif_index):
    lista_media = []
    for i in range(len(lista_dif)):
        lista_media.append((lista_dif[i] + lista_dif_index[i])/2)
    return lista_media

#funções de médias das janelas
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
    media_var1 = []
    media_var2 = []
    lista_media_media = []
    k1_list = []
    k2_list = []
    skew1_list = []
    skew2_list = []
    
    
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
        #medias
        #media em x
        media_index = mediax(lista_dif_index)
        lista_media_x.append(media_index)
        #media em y
        media_pow = mediay(lista_dif)
        lista_media_y.append(media_pow)
        #variancias
        variancia1 = pd.Series(lista_dif_index).var()
        media_var1.append(variancia1)
        variancia2 = pd.Series(lista_dif).var()
        media_var2.append(variancia2)
        #curtose    
        k1 = kurtosis(lista_dif_index)
        k1_list.append(k1)
        k2 = kurtosis(lista_dif)
        k2_list.append(k2)
        
        #coeficiente de assimetria    
        skew_val1 = skew(lista_dif_index)
        skew1_list.append(skew_val1)
        skew_val2 = skew(lista_dif)
        skew2_list.append(skew_val2)
        
        aux += jfs
        aux2 += jfs

    #médias gerais
    media_geral = media(lista_media_y, lista_media_x)
    media_variancia = media(media_var1, media_var2)
    media_k = media(k1_list, k2_list)
    media_skew = media(skew1_list, skew2_list)
        
    
    #plt.plot(k1_list,"o")
    #plt.plot(skew1_list, "o")    
    
    #plt.plot(k2,"o")

    plt.plot(media_k, "--")
    plt.show()
    
    
    