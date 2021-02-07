import numpy as np
import scipy.io.wavfile as sw
import scipy as sc
import matplotlib.pyplot as plt

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
    
    def sifter(self):
        fft = self.fft
        index1 = np.where(fft == np.amax(fft[0:2000]))
        fft[index1] = 0
        index2 = np.where(fft == np.amax(fft[0:2000]))
        return index1[0][0], index2[0][0]

sig = Read('test2.wav')
sig.data = sig.data[0:44100]
sig.fft()
fft = sig.fft
plt.plot(sig.fft[0:2000])
print(sig.sifter())