import pandas as pd

podatki_ch = pd.read_csv ("podatki/Characters.csv", sep=";")
df = pd.DataFrame(podatki_ch)

print(df)