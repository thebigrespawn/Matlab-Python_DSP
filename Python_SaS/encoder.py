import numpy as np
import matplotlib.pyplot as plt
import scipy as sc
import scipy.io.wavfile as sw
import pandas as pd
import os.path

class Parameters:   
#                  1200, 1330, 1460, 1590           #class contains encrypting/decrypting codes
    data = {697 : ['0',  '1',  '2',  '3'],          #Dataframe to make the dictionary
            770 : ['4',  '5',  '6',  '7'],         
            852 : ['8',  '9',  'a',  'b'],          
            941 : ['c',  'd',  'e',  'f']}    
    hx = pd.DataFrame.from_dict(data, orient = 'index',
                                    columns=[1209, 1330, 1477, 1590])
    data_complexity = 2
    gen_samplerate = 44100
    signal_duration = 1
    

class Write(Parameters):
    
    def __init__(self, filename):
        self.filename = filename
        self.string = {}
        self.data_comp = Parameters.data_complexity
        self.samplerate = Parameters.gen_samplerate
        
                
    @staticmethod    
    def wav_constructor(freq1, freq2, filename, samplerate, t):

        T = 1./samplerate
        N = samplerate * t
        w = 2.*np.pi
        t_seq = np.arange(N)*T
        amplitude = (np.iinfo(np.int16).max)/2
        data = amplitude * (np.sin(w*freq1*t_seq) + np.sin(w*freq2*t_seq))
        data_void = 0*np.sin(w*freq1*t_seq)
        sin = np.hstack([data, data_void])
        
        if os.path.isfile(filename):
            f, temp = sw.read(filename)
            sin = np.hstack([temp, sin])
            sw.write(filename, samplerate, sin.astype(np.int16))
        else:
            sw.write(filename, samplerate, sin.astype(np.int16))
            
        return sin
        
    @staticmethod   
    def char_decoder(char):
        listOfPos = [] 
        result = Parameters.hx.isin([char]) 
        seriesObj = result.any() 
        columnNames = list(seriesObj[seriesObj == True].index) 
     
        for col in columnNames: 
            rows = list(result[col][result[col] == True].index) 
            
        for row in rows: 
            listOfPos.append((row, col)) 
            
        freq1 = np.array(listOfPos)[0][0]
        freq2 = np.array(listOfPos)[0][1]
        
        freq1 = int(freq1)
        freq2 = int(freq2)
        return freq1, freq2     
        
    
    
    
    def generate_file(self, par):
        string = list(self.string)
        if par == 'rp':
            print('file replaced')
            os.remove(self.filename)
        else:
            print('writing continued')
        for x in string:
            freq1, freq2 = (Write.char_decoder(x))
            sin = Write.wav_constructor(freq1, freq2, self.filename, self.samplerate, self.signal_duration)    
        return sin
    
sig1 = Write('signal.wav')  
sig1.string = '0123ff56ff78'
sig = sig1.generate_file('rp')  
#Write.wav_constructor(687, 1209, 'signal1.wav')
#Write.wav_constructor(0, 0, 'signal1.wav')
#Write.wav_constructor(941, 1330, 'signal1.wav')
#Write.wav_constructor(0, 0, 'signal1.wav')
#Write.wav_constructor(687, 1209, 'signal1.wav')
#Write.wav_constructor(687, 1209, 'signal1.wav')
#Write.wav_constructor(687, 1209, 'signal1.wav')
    
#sin = Write.wav_constructor(100, 2200, 'signal.wav')    
    

##sig1.data  = sig1.medfil()
###sig1.data = sig1.bandpass(1, 2000)
#sig1.fft = sig1.fft()
#sig1.spike()
##sig = sig1.fft[0 : 2000]
##plt.plot(sig)
##t = 1
##fs = 44100       
##freq1 = 440
##freq2 = 880
##file = "test.wav"
#arr = arr.array[697, 1209]
#a = arr[0]
#b = arr[1]
#hh = Parameters.hx[a][b]  
#    
    
    
#sine_wave1 = np.array([sc.sin(2 * np.pi * 440 * x/44100) for x in range(1 * 44100)])
#sine_wave2 = np.array([sc.sin(2 * np.pi * 880 * x/44100) for x in range(1 * 44100)])
#amplitude = (np.iinfo(np.int16).max)/2
#sin = sine_wave1 + sine_wave2
#sin = amplitude * sin
#sw.write('sintest.wav', 44100, sin.astype(np.int16))
#fs, data = sw.read('sintest.wav')
#fft = np.abs(sc.fft(data))
#plt.plot(fft)






#sin = sine_wave1 + sine_wave2

#fs, data = sw.read('test1.wav')
#fft =  np.abs(sc.fft(data[0:44100]))
#plt.plot(fft[0:2000])



#x =   EncodeString.wav_constructor(100 ,1000 , 'signal.wav')
#s = fft(x)
#plt.plot(s[0:1400])
#sig.spike(sig)





#sig1 = sig1.bandpass(650, 1630)