# -*- coding: utf-8 -*-
"""
Created on Fri May 10 14:17:02 2019

@author: Leonardo
"""

"""
Aplicar principais classificadores KNN, LDK, SVN

"""
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.signal import find_peaks
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew

#Funções

#Médias
#média das médias de duas listas
def media(lista_dif, lista_dif_index):
    lista_media = []
    for i in range(len(lista_dif)):
        lista_media.append((lista_dif[i] + lista_dif_index[i])/2)
    return lista_media

#funções de médias das janelas
def mediax(lista_dif_index): #duas funções iguais, duplicadas apenas para diferenciar durante o código
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
    #diferença picos
    num_peaks = np.zeros(len(peaks)-2)
    for i in range(len(peaks)-2):
        num_peaks[i]=lista[peaks[i]]-lista[peaks[i+1]]
    return num_peaks

def comport(s, lista_dif, peaks):
    for i in range(len(s)-1):
        sub = abs(s[i]-s[i+1])
        lista_dif.append(sub)
    return lista_dif
        
def comport_index(s, lista_dif_index, peaks): # retorna o prórpio intervalo RR
    for i in range(len(s)-1):
        sub_index = abs(peaks[i]-peaks[i+1]) #diferença entre os indices dos picos
        lista_dif_index.append(sub_index)
    return lista_dif_index

def plot_comport(lista, peaks):
    #plot de comportamento dos picos
    s = lista[peaks]
    lista_dif = []
    lista_dif_index = []
    return comport(s, lista_dif, lista_dif_index, peaks)


def entropia (lista):
    return lista

# REFERENCIA
# https://media.readthedocs.org/pdf/python-heart-rate-analysis-toolkit/latest/python-heart-rate-analysis-toolkit.pdf
# x = electrocardiogram()#[2000:4000]
data = pd.read_csv('lista2.txt')
data2 = pd.read_csv('lista3.txt')
fs = 128
J = 30 # janelamento em segundos
jfs = J*fs # 'em segundo'
lista_RR = [] #para ser utilizado na comparação
plot_list1 = []
plot_list2 = []
plot_list3 = []
plot_list4 = []
plot_list5 = []
plot_list6 = []
plot_list7 = []
plot_list8 = []
plot_list9 = []
plot_list10 = []
plot_list11 = []
plot_list12 = []


for w in range(0,17):
    ecg = np.load(data['nome'][w])
    ecg2 = np.load(data2['nome'][w])
    #janelamento
    #precisa ser feito a partir do período de cada janela = 5 min x frequencia amostral = 128hz
    #sendo T o período total da amostra
    T = len(ecg)
    T2 = len(ecg2)    
    aux = 100000
    aux2 = aux + jfs
    lista_media_x1 = [] #listas para armazenamento de dados para 2 variáveis
    lista_media_y1 = []
    lista_media_x2 = []
    lista_media_y2 = []
    media_var1 = []
    media_var2 = []
    media_var3 = []
    media_var4 = []
    lista_media_media1 = []
    lista_media_media2 = []
    k1_list = []
    k2_list = []
    k3_list = []
    k4_list = []
    skew1_list = []
    skew2_list = []
    skew3_list = []
    skew4_list = []
    k5_list = [] #lista para armazenamento de dados do intevalo RR
    k6_list = []
    media_var5 = []
    media_var6 = []
    skew5_list = []
    skew6_list = []
    lista_media_x3 = []
    lista_media_x4 = []    
    media_var5 = []
    media_var6 = []
        
    while(aux2<=len(ecg)):                
        x = ecg[aux:aux2]      
        #limiar
        threshold = np.repeat(3*np.std(x), len(x))
        
        #obtendo picos
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
        lista_media_x1.append(media_index)
        #media em y
        media_pow = mediay(lista_dif)
        lista_media_y1.append(media_pow)
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
        
        #######################################################################
        
        aux += jfs
        aux2 += jfs
        
    #médias gerais 1
    media_geral = media(lista_media_y1, lista_media_x1)
    media_variancia = media(media_var1, media_var2)
    media_k = media(k1_list, k2_list)
    media_skew = media(skew1_list, skew2_list)       
    
    pplot1 = mediax(media_k)
    plot_list1.append(pplot1)
    
    pplot2 = mediax(media_variancia)
    plot_list2.append(pplot2)
    
    pplot3 = mediax(media_skew)
    plot_list3.append(pplot3)
    
    
    ###########################################################################    
    aux = 120000
    aux2 = aux + jfs
    
    while(aux2<=len(ecg2)):                
        k = ecg2[aux:aux2]        
        #limiar
        threshold = np.repeat(3*np.std(x), len(x))     
        
        #######################################################################
        
        #obtendo picos
        peaks2 = peaks(k)       
        p = k[peaks2]
        numero2 = num_peaks(x, peaks2)
        lista_dif2 = []
        comport2 = comport(p, lista_dif2, peaks2)
        lista_dif_index2 = []
        comport_index2 = comport_index(p, lista_dif_index2, peaks2)
        #medias
        #media em x
        media_index2 = mediax(lista_dif_index2)
        lista_media_x2.append(media_index2)
        #media em y
        media_pow2 = mediay(lista_dif2)
        lista_media_y2.append(media_pow2)
        #variancias
        variancia3 = pd.Series(lista_dif_index2).var()
        media_var3.append(variancia3)
        variancia4 = pd.Series(lista_dif2).var()
        media_var4.append(variancia4)
        #curtose    
        k3 = kurtosis(lista_dif_index2)
        k3_list.append(k3)
        k4 = kurtosis(lista_dif2)
        k4_list.append(k4)
        
        #coeficiente de assimetria    
        skew_val3 = skew(lista_dif_index2)
        skew3_list.append(skew_val3)
        skew_val4 = skew(lista_dif2)
        skew4_list.append(skew_val4)
        
        aux += jfs
        aux2 += jfs    
    
    
    #médias gerais 2
    media_geral2 = media(lista_media_y2, lista_media_x2)
    media_variancia2 = media(media_var3, media_var4)
    media_k2 = media(k3_list, k4_list)
    media_skew2 = media(skew3_list, skew4_list)        
    
    #plt.plot(k1_list,"o")
    #plt.plot(skew1_list, "o")    
    
    #plt.scatter(media_var1, media_var2)
    
    #plt.plot(k2,"o")
    #plt.plot(media_geral, "--")
    #plt.plot(media_variancia, "o")
    #plt.plot(media_k, "o")
    
    #plt.plot(media_skew, "o")
    #plt.plot(media_k, "o")
    #plt.show()
    #plt.plot(media_k2, "o")
    #plt.plot(media_skew2, "o")
    
    #fig = plt.figure()
    #ax = Axes3D(fig)
    #ax.plot(media_k, media_variancia, media_skew, "o")
    #ax.plot(media_k2, media_variancia2, media_skew2, "o")
    
        
    pplot4 = mediax(media_k2)
    plot_list4.append(pplot4)
    
    pplot5 = mediax(media_variancia2)
    plot_list5.append(pplot5)
    
    pplot6 = mediax(media_skew2)
    plot_list6.append(pplot6)
    

    #intervalo RR
    aux = 120000
    aux2 = aux + jfs
    
    while(aux2<=len(ecg)):                
        x = ecg[aux:aux2]
    
        #obtendo picos
        peaks12 = peaks(x)       
        s = x[peaks12]
        lista_dif_index12 = []
        comport_index1 = comport_index(s, lista_dif_index12, peaks12)
        
        #medias
        #media em x
        media_index12 = mediax(lista_dif_index12)
        #variancias
        variancia5 = pd.Series(lista_dif_index12).var()
        media_var5.append(variancia5)
        
        #curtose    
        k5 = kurtosis(lista_dif_index12)
        k5_list.append(k5)
        
        #coeficiente de assimetria    
        skew_val5 = skew(lista_dif_index12)
        skew5_list.append(skew_val5)       
    
        aux += jfs
        aux2 += jfs 
    
    pplot7 = mediax(k5_list)
    plot_list7.append(pplot7)
    
    pplot8 = mediax(media_var5)
    plot_list8.append(pplot8)
    
    pplot9 = mediax(skew5_list)
    plot_list9.append(pplot9)
    
    aux = 120000
    aux2 = aux + jfs
    
    while(aux2<=len(ecg)):                
        x = ecg2[aux:aux2]
    
        #obtendo picos
        peaks22 = peaks(x)       
        s = x[peaks22]
        lista_dif_index22 = []
        comport_index22 = comport_index(s, lista_dif_index22, peaks22)
        
        #medias
        #media em x
        media_index22 = mediax(lista_dif_index22)
        #variancias
        variancia6 = pd.Series(lista_dif_index22).var()
        media_var6.append(variancia6)
        
        #curtose    
        k6 = kurtosis(lista_dif_index22)
        k6_list.append(k6)
        
        #coeficiente de assimetria    
        skew_val6 = skew(lista_dif_index22)
        skew6_list.append(skew_val6)       
    
        aux += jfs
        aux2 += jfs 
        
    pplot10 = mediax(k6_list)
    plot_list10.append(pplot10)
    
    pplot11 = mediax(media_var6)
    plot_list11.append(pplot11)
    
    pplot12 = mediax(skew6_list)
    plot_list12.append(pplot12)
        
    
fig = plt.figure()
fig2 = plt.figure()
ax = Axes3D(fig)
ar = Axes3D(fig2)
ax.plot(plot_list1, plot_list2, plot_list3, "o")
ax.plot(plot_list4, plot_list5, plot_list6, "o") 
ar.plot(plot_list7, plot_list8, plot_list9, "x")
ar.plot(plot_list10, plot_list11, plot_list12, "x")
plt.show()





    
    
    