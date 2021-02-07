clc;
close all;
clear ; %clear all previous records in matlab
filename = 'Project1_v2.wav';%PLEASE TYPE YOUR AUDIO FILE NAME HERE
[data, Fs] = audioread(filename);%reading audiofile and converting it into table

data = medfilt1(data,10);%median filter to make signal smoother
data = bandpass(data, [670 1500], Fs);%bandpass filter to reduce the overall noise

envelope = imdilate(abs(data), true(1500, 1));%definiing loud regions' boundaries
quietParts = envelope > 0.04;
beginning = strfind(quietParts',[0 1]);%set of load region beginnings
ending = strfind(quietParts', [1 0]);%set of loud region endings
plot(data);% plotting the filtered signal

disp("Your desired number is:");

disp(getNumber(1, ending(1, 1)-1000, data));%displaying first interval as 
                                            %previous fuction didn't
                                            %returned the first beginning

for n = 1:+1:length(beginning)%for loop to find the numbers of every interval 
b = beginning (1,n) + 1000;   %and diplay them
e = ending(1,n+1) - 1000; %cutting corners of every interval by 1000 to make the more clear
number = getNumber(b, e, data);%function with fft which gets beginning and ending coordinates
disp(number);
end

function CC = closestColumn(C)%as the fft cannot make analysis without error
    Column = [1209 1336 1477];%we need to correct them manually
    v1 = 1000;
    for n=1:+1:3
    v = C - Column(n);
        if abs(v) < v1
        CC = Column(n);
        v1 = v; 
        end    
    
    end

end

function CR = closestRow(R)%finding the actual frequencies by finding the closest one
    Row = [697 770 852 941];
    v1 = 1000000;
    for n=1:+1:4
    v = R- Row(n);
        if abs(v)<v1
        CR = Row(n);
        v1 = v; 
        end    
    
    end

end

function number = getNumber(b, e, data)

base(697, 1209) = 1;%declaring the frequency - number base
base(697, 1336) = 2;
base(697, 1477) = 3;
base(770, 1209) = 4;
base(770, 1336) = 5;
base(770, 1477) = 6;
base(852, 1209) = 7;
base(852, 1336) = 8;
base(852, 1477) = 9;
base(941, 1336) = 0;

data_fft = fft(data(b:e));%Fast Fourier Transform over defined intervals of audio

[M1, R] = max(data_fft(1:942));%Finding the first frequency
data_fft(R) = 0;
[M2, C] = max(data_fft(1:1480));%finding the second frequency
C = closestColumn(C);%ERROR CORRECTION
R = closestRow(R);
number = base(R, C);%desired number for its iteration
end

