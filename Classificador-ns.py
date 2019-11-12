#as duas bases estão nessa aplicação
#import matplotlib
#import matplotlib.mlab as mlab
#import matplotlib.gridspec as gridspec
#from scipy.misc import electrocardiogram
#from scipy import stats
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
import numpy as np
from scipy.stats import kurtosis, skew

#Funções

#Média
def media(lista):
    return (sum(lista)/len(lista))

def comportamento(s, lista_dif, lista_dif_index, peaks):
    for i in range(len(s)-1):
        sub = abs(s[i]-s[i+1])
        sub_index = abs(peaks[i]-peaks[i+1])
        lista_dif.append(sub)
        lista_dif_index.append(sub_index)
        
def peaks(lista):
    
    #distancia = frequencia amostral
    peaks, _ = find_peaks(lista, distance=fs//2)
    np.diff(peaks)
    
    return peaks

def num_peaks(lista, peaks):    
    #número de picos
    num_peaks = np.zeros(len(peaks)-2)
    for i in range(len(peaks)-2):
        num_peaks[i]=lista[peaks[i]]-lista[peaks[i+1]]
    return num_peaks

def plot_comport(lista, peaks):
    #plot de comportamento dos picos
    s = lista[peaks]
    lista_dif = []
    lista_dif_index = []
    return comportamento(s, lista_dif, lista_dif_index, peaks)   
        
    
# REFERENCIA
# https://media.readthedocs.org/pdf/python-heart-rate-analysis-toolkit/latest/python-heart-rate-analysis-toolkit.pdf
# x = electrocardiogram()#[2000:4000]
data = pd.read_csv('lista2.txt')
data2 = pd.read_csv('lista3.txt')
fs = 128
# ecg = np.array(data['ECG'])#.reshape(1,len(data['ECG']))
#for i in range(len(data)):
#
#    ecg = np.load(data['nome'][i])
#    x = ecg[:1280*4]
#    # distance = frequencia amostral
#    peaks, _ = find_peaks(x, distance=fs//2)
#    np.diff(peaks)
#    # limiar
#    aux = np.repeat(np.std(x), len(x))
#
#    fig = plt.figure(constrained_layout=True)
#    gs = gridspec.GridSpec(2, 3, figure=fig)
#    ax = fig.add_subplot(gs[0, :])
#    ax.plot(x)
#    ax.plot(peaks, x[peaks], "x")
#    ax.plot(aux,"--",color="gray")
#    ax.set_xlabel('time [s]')
#    ax.set_ylabel('signal')
#
#    ax3 = fig.add_subplot(gs[1, 1])
#    ax3.boxplot(x[peaks])
#    ax3.set_ylabel('')
#
#    plt.show()
for w in range(0,1):
    ecg = np.load(data['nome'][w])
    ecg2 = np.load(data2['nome'][w])
    x = ecg[120000:140000]
    teste = ecg[120000:140000]
    k = ecg2[120000:140000]
    
    # distance = frequencia amostral
    peaks1, _ = find_peaks(x, distance=fs//2)
    peaks2, _ = find_peaks(k, distance=fs//2)
    np.diff(peaks1)
    np.diff(peaks2)
    
    #numero de picos
    num_peaks1 = np.zeros(len(peaks1)-2)
    for i in range(len(peaks1)-2):
        num_peaks1[i]=x[peaks1[i]]-x[peaks1[i+1]]
        
    num_peaks2 = np.zeros(len(peaks2)-2)
    for i in range(len(peaks2)-2): 
        num_peaks2[i]=x[peaks2[i]]-x[peaks2[i+1]]

    # limiar
    aux = np.repeat(3*np.std(x), len(x))

    """
    #gráfico principal para picos
    fig = plt.figure(constrained_layout=True)
    gs = gridspec.GridSpec(2, 3, figure=fig)
    ax = fig.add_subplot(gs[0, :])
    ax.plot(x)
    ax.plot(peaks, x[peaks], "x")
    #ax.plot(peaks, x[ab],"o",color="red")
    ax.plot(aux, "--", color="gray")
    """

    #ax3 = fig.add_subplot(gs[1, 1]) #gráficos dos picos
    #ax3.boxplot(x[peaks])

    # print (x[peaks]) #valor picos

    #plot de comportamento dos picos
    s = x[peaks1]
    lista_dif1 = []
    lista_dif_index1 = []
    comportamento(s, lista_dif1, lista_dif_index1, peaks1)
    
    t = np.arange(len(lista_dif1))
    t2 = np.arange(len(lista_dif_index1))
        
    s2 = k[peaks2]
    lista_dif2 = []
    lista_dif_index2 = []
    comportamento(s2, lista_dif2, lista_dif_index2, peaks2)
    
    t3 = np.arange(len(lista_dif2))
    t4 = np.arange(len(lista_dif_index2))
    
    
    #media dos dois pontos encontrados para formação de um só vetor
    lista_media1 = []
    for i in range(len(lista_dif1)):
        lista_media1.append((lista_dif1[i] + lista_dif_index1[i])/2)
        
    lista_media2 = []    
    for i in range(len(lista_dif2)):
        lista_media2.append((lista_dif2[i] + lista_dif_index2[i])/2)
    
    #variancias
    variancia1 = pd.Series(lista_media1).var()
    variancia2 = pd.Series(lista_media2).var()
    
    #curtose    
    k1 = kurtosis(lista_media1)
    k2 = kurtosis(lista_media2)
    
    #coeficiente de assimetria    
    skew1 = skew(lista_media1)
    skew2 = skew(lista_media2)
    
    #informações sobre os sinais:    
    print(media(num_peaks1))   
    
    #fig, ax4 = plt.subplots()
    #ax4.plot(t,lista_dif)

    #fig, ax5 = plt.subplots()
    #ax5.plot(lista_dif_index1,lista_dif1,"o")

    #ax4.set(xlabel='tempo (s)', ylabel = 'Diferença entre Picos')
    #ax4.grid()

    #ax5.set(xlabel='tempo (s)', ylabel = 'Diferença de index')
    #ax5.grid()
    #plt.scatter(lista_dif_index1,lista_dif1)
    
    #plt.scatter(lista_dif_index2,lista_dif2)
    #plt.boxplot([lista_dif1,lista_dif2])

    plt.boxplot([lista_media1[:233], lista_media2[:233]])

    plt.show()
    
