from funkcije import sound
from funkcije import text
import pandas as pd
import time
#import streamlit as st

#Nastavljeno da sve munuti zajema zvok.
#20sec posluša in nata analiza.
#Pričakujem okoli 4-6 citatiov.
def main():
    ts=time.time()
    tf=time.time()
    cc=0
    #st.write("# Zvočna arheologija?")
    while ((tf-ts)<2*60): 
        #st.write("## Izkopavanje?")
        tabela=pd.read_excel('data/Pesmi.xlsx',engine="openpyxl")
        #tabela=pd.read_excel("data//Pesmi.xlsx"
        rezultat = sound.get_text_from_audio(cc,20)
        #st.write(rezultat)
        
        beri=text.analiza(rezultat,tabela)
        #st.write("-------------------------------------------------------------------")
        tf=time.time()
        cc+=1

if __name__=="__main__":
    main()