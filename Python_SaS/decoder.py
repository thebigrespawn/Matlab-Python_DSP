import numpy as np
import scipy.io.wavfile as sw
import scipy as sc
import scipy.signal as ss
import matplotlib.pyplot as plt
import pandas as pd


class Parameters:   
#                  1200, 1330, 1460, 1590           #class contains encrypting/decrypting codes
    data = {697 : ['1',  '2',  '3',  '3'],          #Dataframe to make the dictionary
            770 : ['4',  '5',  '6',  '7'],         
            852 : ['7',  '8',  '9',  'b'],          
            941 : ['c',  '0',  'e',  'f']}         
    hx = pd.DataFrame.from_dict(data, orient = 'index',
                                    columns=[1209, 1330, 1477, 1590])

class Tools:
    @staticmethod
    def noise(data):
        noise = np.random.uniform(low=-10000, high=10000, size=(sig.frames))
        noised_data = data + noise
        return noised_data
    def pos(data):
        return [x for x in data if x > 0] or None
    
    def neg(data):
        return [x for x in data if x < 0] or None
    
        fil = sc.signal.butter(2, [640, 1600], 'bandpass', output = 'sos',fs = samp)
        data_filtered = sc.signal.sosfilt(fil, data)
        return data_filtered
    
    def split(data, noise, frames):
        val = 1
        f = int(frames/1000)
        bin_data = np.where(abs(data) > noise, 1, 0)
        for x in range (0, f):
            arr = bin_data [x*1000 : (x+1)*1000]
            if val in arr:
                bin_data[x*1000 :(x+1)*1000] = 1              
        return bin_data
    
    
class Read:
                        #Read class to extract data from the file, needs filename as argument to operate
    def __init__(self, filename):  
        self.filename = filename   
        self.samp_freq, self.data = sw.read(self.filename)
        self.frames = len(self.data)
        self.fft

    def fft(self):      #fft method to make fast fourier transform on object's data
        fft_data = (sc.fft(self.data))
        fft_real = np.abs(fft_data/self.frames) #as sc.fft returns complex values too, we need only real part
        self.fft = fft_real
        return fft_real
    
    def interval_grabber(self, data):
        noise = np.average(Tools.pos(sig.data))*1.5
        bin_data = Tools.split(data, noise, self.frames)
        return bin_data
        
    def sifter(self):       #sifter separates 2 strongest frequencies from fft data set to ddecode the message in future
        fft = self.fft
        index1 = np.where(fft == np.amax(fft[0:2000]))
        fft[index1] = 0
        index2 = np.where(fft == np.amax(fft[0:2000]))
        return index1[0][0], index2[0][0]
    
    def decoder(self):      #decoder takes 2 frequencies and finds related symbol in Parameters encoding library
        f1, f2 = self.sifter()
        letter = Parameters.hx[f1][f2]
        return letter    

sig = Read('signal.wav')
plt.plot(sig.data)
sig.data = Tools.noise(sig.data)
sig.data = Tools.bandpass(sig.data, 44100)
data = sig.interval_grabber(sig.data)

#data1 = sig.data
#plt.plot(sig.data)
#mean1 = np.average(Tools.pos(sig.data))*1.5
#data = cn(data1, sigma = 10)
##fft = sig.fft
#plt.plot(sig.fft[0:2000])
#print(sig.decoder())
