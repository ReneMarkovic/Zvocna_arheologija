#text.py
import random
import streamlit as st
import time
import gtts
from playsound import playsound
from googletrans import Translator, constants
from os import environ
import codecs
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from pygame import mixer


def analiza(rezultat,tabela):
    try:
        pisi=codecs.open("Rezultat_tekst.txt","a",'UTF-8')
    except:
        pisi=codecs.open("Rezultat_tekst.txt","w+",'UTF-8')
        pisi.close()
        pisi=codecs.open("Rezultat_tekst.txt","a",'UTF-8')
        
    print("Iskanje pripadajoče pesmi.")
    rezultat=rezultat.replace(" ","")
    rezultat=''.join([i for i in rezultat if i.isalpha])
    print("Zaznano je sporočilo:",rezultat)
    ic=0
    OK=0
    for i in range(len(rezultat)-3):
        key=rezultat[i:i+3]
        xx=tabela[tabela["Pesem_find"].str.contains(key)]["Pesem"].values
        if len(xx)>0:
            x=xx
            beri=random.choice(x)
            st.write(beri)
            print(rezultat, key, beri,file=pisi,sep="\t")
            #translation = translator.translate(beri, src="sl", dest="en")
            #print(translation)
            tts = gtts.gTTS(beri, lang="sk")
            try:
                tts.save("data\hello_%02d.mp3"%ic)
                mixer.init()
                mixer.music.load("data\hello_%02d.mp3"%ic)
                mixer.music.play()
                OK=1
                i=10000000
                print(i)
                while mixer.music.get_busy():  # wait for music to finish playing
                    time.sleep(0.5)
                
                playsound()
                ic+=1
                print(ic)
                return beri
            except:
                ic+=1
        if OK:
            break 
    pisi.close()
    return beri