import pandas as pd

podatki_characters = pd.read_csv(r'podatki/Characters.csv', sep=";")
df = pd.DataFrame(podatki_characters)

students = df.loc[df['Job'] == "Student"]
professors = df.loc[df['Job'] == r'.*Professor.*']
#for i in range(len(df)):
#    if df["Job"] == "Student":df.loc[df['Job'] == "Student"]
#        students = df
        #df['Job'] = df['Job'].replace(['Headmaster', 'Keeper of Keys and Grounds | Professor'], 'Professor')
print(students)
print(professors)
