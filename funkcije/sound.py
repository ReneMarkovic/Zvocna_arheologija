#sound.py
import sounddevice as sd
from scipy.io.wavfile import read
from scipy.io.wavfile import write
import scipy.io.wavfile as wavf
from scipy import signal
import numpy as np
import time

device = sd.default.device[0]
print("Default device:", device)

'''devices = sd.query_devices()
for idx, device in enumerate(devices):
    print(f"Device index: {idx}, Device name: {device['name']}")'''

morsetab = {
   'a':'.-',    'b':'-...',
   'c':'-.-.',  'd':'-..',
   'e':'.',     'f':'..-.',
   'g':'--.',   'h':'....',
   'i':'..',    'j':'.---',
   'k':'-.-',   'l':'.-..',
   'm':'--',    'n':'-.',
   'o':'---',   'p':'.--.',
   'q':'--.-',  'r':'.-.',
   's':'...',   't':'-',
   'u':'..-',   'v':'...-',
   'w':'.--',   'x':'-..-',
   'y':'-.--',  'z':'--..',
   '0':'-----', ',':'--..--',
   '1':'.----', '.':'.-.-.-',
   '2':'..---', '?':'..--..',
   '3':'...--', ';':'-.-.-.',
   '4':'....-', ':':'---...',
   '5':'.....',  "'":'.----.',
   '6':'-....', '-':'-....-',
   '7':'--...', '/':'-..-.',
   '8':'---..', '(':'-.--.-',
   '9':'----.', ')':'-.--.-',
   '':'|',      '_':'..--.-',
}

morse_latter={}
for x in morsetab:
    morse_latter[morsetab[x]]=x

def get_rms(block):
        return np.sqrt(np.mean(block**2))

def capture_audio(cc,duration):
    print("Pričenjam z zajemanjem okolja.")
    fs = 44100  # Sample rate
    seconds = duration  # Duration of recording
    


    # Create a progress bar for the recording
    myrecording = sd.rec(int(seconds * fs),
                         samplerate=fs,
                         channels=2)

    sd.wait()  # Wait until recording is finished
    write("data\\rec_sound_%03d.wav"%(cc), fs, myrecording)  # Save as WAV file
    
    
    sr=read("data\\rec_sound_%03d.wav"%(cc))[0]
    a=np.array(read("data\\rec_sound_%03d.wav"%(cc))[1],dtype=float)
    x=[i/sr for i in range(len(a))]

    w=int(sr*1)

    nw=int(len(a)/w)
    #print(nw)
    norm_a=np.empty_like(a[:,1])
    #print(norm_a)
    #print(a[:,1])
    th=0.01
    th_a=np.empty_like(a[:,1])
    for i in range(nw):
        #print(i*w,(i+1)*w)
        norm_a[i*w:(i+1)*w]=a[i*w:(i+1)*w,0]/max(abs(a[i*w:(i+1)*w,0]))

    cut=int(44100/6)# 0.5s/6

    ns=int(len(a)/cut)
    for i in range(ns):
        th_a[i*cut:(i+1)*cut]=get_rms(norm_a[i*cut:(i+1)*cut])#np.mean(abs(norm_a[i*cut:(i+1)*cut]))
        #print(get_rms(norm_a[i*cut:(i+1)*cut]))

    np.iinfo(np.int16).max
    amplitude = np.iinfo(np.int16).max
    norm_a=norm_a*amplitude
    out_f = 'data\out_normalized.wav'
    write(out_f, sr, norm_a.astype(np.int16))
    f, t, Sxx = signal.spectrogram(norm_a, sr)
    fac=[]
    for i in range(len(t)):
        fac.append(np.mean(Sxx[0:10,i])/np.mean(Sxx[10::,i]))
    return fac

fsr=3937/20
print(fsr)
text=""

def get_text_from_audio(cc,duration):
    print("Ekstrahiranje sporočila iz posnetka.")
    text=""
    fac=capture_audio(cc,duration)
    for j in range(1,18,1):
        m=''
        y=fac[int(j*196.85):int((j+1)*196.85)]/max(fac[int(j*196.85):int((j+1)*196.85)])
        for i in range(1,7):
            std=np.std(y[int((i-1)/6*196.85):int((i)/6*196.85)])
            mean=np.mean(y[int((i-1)/6*196.85):int((i)/6*196.85)])
            mmax=max(y[int((i-1)/6*196.85):int((i)/6*196.85)])
            metrica=np.sum(y[int((i-1)/6*196.85):int((i)/6*196.85)] >= np.mean(y))
            if metrica<1:
                m+=" "
            elif metrica<10:
                m+="."
            else:
                m+="-"
            #print(len(fac[int(j*196.85)+int((i-1)/6*196.85):int(j*196.85)+int((i)/6*196.85)]))
        if m[0]==" ":
            m=m[1::]
        while m[-1]==" ":
            m=m[0:len(m)-1]
        m=m.split(" ")
        #print(m)
        for mm in m:
            try:
                text+=morse_latter[mm]
                #print(morse_latter[mm])
            except:
                #print("Ni šlo")
                OK=1
                iii=1
                while OK:
                    try:
                        text+=morse_latter[mm[0:iii]]
                        #print(morse_latter[mm[0:iii]])
                        OK=0
                    except:
                        #print("Ni šlo")
                        pass
                    iii+=1
                    if iii>6:
                        OK=0
                    
                text+=" "
        #print("----------------------------")
    return text