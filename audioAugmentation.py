import numpy as np
import pandas as pd
from scipy.io.wavfile import write
import librosa
import threading
import time

savePath = '/home/neko/Desktop/Crack Former Project/Data/Synthetic Data/'
path = '/home/neko/Desktop/Crack Former Project/Data/Trimmed Raw Data/'

df = pd.read_csv('/home/neko/Desktop/Crack Former Project/Data_2021_Features.csv')
df.dropna(inplace = True)
df.drop_duplicates(subset='Original_FN', inplace=True)
df.set_index('Filename', inplace=True)
df = df[~(df['Length'] <= 0.249977)]
a = np.array_split(df, 8)

window = np.load("/home/neko/Desktop/Crack Former Project/Data/window.npy", allow_pickle=True)

# def Synthetic_data(data):
# for f in df.index[0:1]:
for f in df.index:
    # print(f)
    filename = f.split('.')[0]
    # print(f'Reading audio: {path+f}')
    x, fr = librosa.load(path+f)
    for i in range(len(window)):
        for j in range(len(window[i])):
            # print(f'Mixing with noise {i}, window {j}')
            # print(len(window[i][j]))
            mixed = (x*2)+window[i][j]          
            write(savePath+filename+'__%s_%s.wav'%(i,j), fr, mixed)

# for i in range (0,len(a)):
#     augment = threading.Thread(
#         target=Synthetic_data,
#         args= (a[i],)
    
#     daemon=True,
# ) 
# Synthetic_data(df)
# augment.start()