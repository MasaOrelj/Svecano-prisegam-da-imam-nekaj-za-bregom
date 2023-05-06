import pandas as pd
import re
from pandas import DataFrame

from Database import Repo
from Modeli import *
from typing import Dict
from re import sub
import dataclasses

podatki_characters = pd.read_csv(r'Data/Characters.csv', sep=";")
df = pd.DataFrame(podatki_characters)


professors = df[df['Job'].str.match('(.*(Professor).*)|(Headmaster)|(Defence Against the Dark Arts(1991-1992))|(Defence Against the Dark Arts(1992-1993))|(Headmistress of Beauxbatons Academy of Magic)|(Caretaker of Hogwarts)|(Matron at Hogwarts School)|(Flying Instructor at Hogwarts)|(Librarian at Hogwarts)|(Astronomer at Hogwarts)')== True]
professors.drop(columns=["Id", "Gender", "Job", "Wand", "Patronus", "Species", "Blood status", "Hair colour", "Eye colour", "Loyalty", "Skills", "Birth", "Death"], inplace=True)
professors.columns= ['name', 'house']
professors2 = professors.copy()

students1 = df[df['Job'].str.match('(.*(Professor).*)|(Headmaster)|(Defence Against the Dark Arts(1991-1992))|(Defence Against the Dark Arts(1992-1993))|(Headmistress of Beauxbatons Academy of Magic)|(Caretaker of Hogwarts)|(Matron at Hogwarts School)|(Flying Instructor at Hogwarts)|(Librarian at Hogwarts)|(Astronomer at Hogwarts)')== False]
students2 = df[df['Job'].isna()]
students_and_muggles = pd.concat([students1, students2], axis=0)
muggles = df[df['Name'].str.match('.*(Dursley)')== True]
students = students_and_muggles[(students_and_muggles["Id"] != 120) & (students_and_muggles["Id"] != 121) & (students_and_muggles["Id"] != 122) & (students_and_muggles["Id"] != 123)]



repo = Repo()

def uvozi_v_sql(df, ime):
    repo.df_to_sql_create(df, ime, add_serial=True, use_camel_case=True)
    repo.df_to_sql_insert(df, ime, use_camel_case=True)

uvozi_v_sql(professors2, "professors")




