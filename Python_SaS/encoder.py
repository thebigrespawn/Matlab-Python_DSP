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
    data_complexity = 2     #you can decode your data with more than 1 frequency, just mention it there
    gen_samplerate = 44100  #sampling frequency of created file
    signal_duration = 1     #intervas' longevity
    

class Write(Parameters):
    
    def __init__(self, filename):               # extracting all necessary data from file by creatng object
        self.filename = filename
        self.string = {}
        self.data_comp = Parameters.data_complexity
        self.samplerate = Parameters.gen_samplerate
        
                
    @staticmethod    
    def wav_constructor(freq1, freq2, filename, samplerate, t):     # method to create the wav file itself
        T = 1./samplerate
        N = samplerate * t
        w = 2.*np.pi
        t_seq = np.arange(N)*T
        amplitude = (np.iinfo(np.int16).max)/2
        
        data = amplitude * (np.sin(w*freq1*t_seq) + np.sin(w*freq2*t_seq))  #create 2 sinusoids with desirable frequencies to encode letter
        data_void = 0*np.sin(w*freq1*t_seq)  #create silent region to properly analyse signal in future
        sin = np.hstack([data, data_void])  #stack loud and silent regions
        
        if os.path.isfile(filename):            #check whether file exists
            f, temp = sw.read(filename)         #if it exists combine new encoded letter with it
            sin = np.hstack([temp, sin])
            sw.write(filename, samplerate, sin.astype(np.int16))
        else:
            sw.write(filename, samplerate, sin.astype(np.int16)) #else create new file
            
        return sin
        
    @staticmethod   
    def char_decoder(char):         #method to find which frequencies are assigned to the following letter duing the encoding process
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
        freq2 = int(freq2)      #returns frequencies from table in "Parameters"
        return freq1, freq2     
        
    
    
    
    def generate_file(self, par):           # method to run all the methods in collaboration
        string = list(self.string)
        if par == 'rp':
            print('file replaced')
            os.remove(self.filename)
        else:
            if par =='cw':
                print('writing continued')
        for x in string:
            freq1, freq2 = Write.char_decoder(x)
            sin = Write.wav_constructor(freq1, freq2, self.filename, self.samplerate, self.signal_duration)    
        return sin
    
sig1 = Write('signal.wav')  #driver code
sig1.string = 'bca01134ced'
sig = sig1.generate_file('rp') #choose writing mode from rp - replace file with new and cw - continue writing in existing file
