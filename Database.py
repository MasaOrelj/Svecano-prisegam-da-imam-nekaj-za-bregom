import pandas as pd

podatki_characters = pd.read_csv(r'podatki/Characters.csv', sep=";")
df = pd.DataFrame(podatki_characters)

print(df)
