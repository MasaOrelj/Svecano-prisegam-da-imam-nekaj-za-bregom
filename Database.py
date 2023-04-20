import pandas as pd

podatki_ch = pd.read_csv ("C:/Users/mo6404/Desktop/Projekt_baze/Svecano-prisegam-da-imam-nekaj-za-bregom/podatki/Characters.csv", sep=";")
df = pd.DataFrame(podatki_ch)



print(df)