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
    lower = list(data.keys())    
    hx = pd.DataFrame.from_dict(data, orient = 'index',
                                    columns=[1209, 1330, 1477, 1590])
    upper = list(hx.keys())
    highest_freq = max(upper)
    lowest_freq = min(lower)


class Tools:
    
    def noise(data):
        noise = np.random.uniform(low=-10000, high=10000, size=(sig.frames))
        noised_data = data + noise
        return noised_data
    
    def bandpass(data, samp):
        fil = sc.signal.butter(1, [500, 2000], 'bandpass', output = 'sos',fs = samp)
        data_filtered = sc.signal.sosfilt(fil, data)
        return data_filtered
    
    def approximate(array1, array2, val1, val2):
        array1 = np.asarray(array1)
        idx1 = (np.abs(array1 - val1)).argmin()
        array2 = np.asarray(array2)
        idx2 = (np.abs(array2 - val2)).argmin()
        return array1[idx1] , array2[idx2]      
    
    
    def split(data, treshold, frames):
        try:
            data = np.array(data)
            data[0] = 0
            y = 0
            f = int(frames/1000)
            beginnings = {}
            endings = {}
            bin_data = np.where(abs(data) > treshold, 1, 0)
            for x in range (0, f):
                arr = bin_data [x*1000 : (x+1)*1000]
                if 1 in arr:
                    bin_data[x*1000 :(x+1)*1000] = 1
                    if bin_data[x*1000 - 1] == 0:
                        y = y+1
                        beginnings[x] = x*1000
                    else:
                        if bin_data[x*1000 - 1] == 1:
                    
                            endings[y] = x*1000
            return beginnings, endings
        except:
            print('error split')
            
            
    
    def fft(data, frames, beg, end): #fft method to make fast fourier transform on object's data
        try:
            segment_fft = np.abs((sc.fft(data[beg+1000:end-1000]))/frames)[0:20000]
            return segment_fft
        except:
            print('error fft')
    
    def sifter(segment_fft):       #sifter separates 2 strongest frequencies from fft data set to ddecode the message in future

        index1 = np.where(segment_fft == np.amax(segment_fft))[0][0]
        segment_fft[index1] = 0
        index2 = np.where(segment_fft == np.amax(segment_fft))[0][0]
        if index1>index2:
            return index2, index1
        
        else:
            return index1, index2
    

    
    
    
class Read:
                        #Read class to extract data from the file, needs filename as argument to operate
    def __init__(self, filename):  
        self.filename = filename   
        self.samp_freq, self.data = sw.read(self.filename)
        self.frames = len(self.data)
        
        
    def interval_grabber(self):
        noise_treshold = np.average(abs(self.data))*1.4
        beg, end = Tools.split(self.data, noise_treshold, self.frames)
        length = len(beg)
        beg = np.asarray(list(beg.values()))
        end = np.asarray(list(end.values()))
        return beg, end, length

        
    
    def decode(self):
        string={}
        beg, end, length = self.interval_grabber()
        
        
        for i in range(0, length):
            segment_fft = Tools.fft(sig.data, sig.frames, beg[i], end[i])
            index1, index2 = Tools.sifter(segment_fft)
            index1, index2 = Tools.approximate(Parameters.lower, Parameters.upper, index1, index2)
            letter = Parameters.hx[index2][index1]
            string[i] = letter
            
        return string


sig = Read('signal.wav')
string = sig.decode()














#sig.data = Tools.bandpass(sig.data, sig.frames)
#data = sig.data
#beg, end, length = sig.interval_grabber()
#string = sig.to_string()
#u = Parameters.highest_freq
#d = Parameters.lowest_freq
#beg, end = Tools.split(sig.data, 20000, sig.frames)
#beg = np.asarray(list(beg.values()))[0]
#end = np.asarray(list(end.values()))[0]
#segment_fft = Tools.fft(sig.data, sig.frames, beg, end)
#index1 , index2 = Tools.sifter(segment_fft)


#data1 = sig.data
#plt.plot(sig.data)
#mean1 = np.average(Tools.pos(sig.data))*1.5
#data = cn(data1, sigma = 10)
##fft = sig.fft
#plt.plot(sig.fft[0:2000])
#print(sig.decoder())
