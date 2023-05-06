import pandas as pd
import re
from pandas import DataFrame

from Data.Database import Repo
from Data.Modeli import *
from typing import Dict
from re import sub
import dataclasses

podatki_characters = pd.read_csv(r'Data/Characters.csv', sep=";")
df = pd.DataFrame(podatki_characters)

professors = df[df['Job'].str.match('(.*(Professor).*)|(Headmaster)|(Defence Against the Dark Arts(1991-1992))|(Defence Against the Dark Arts(1992-1993))|(Headmistress of Beauxbatons Academy of Magic)|(Caretaker of Hogwarts)|(Matron at Hogwarts School)|(Flying Instructor at Hogwarts)|(Librarian at Hogwarts)|(Astronomer at Hogwarts)')== True]
students1 = df[df['Job'].str.match('(.*(Professor).*)|(Headmaster)|(Defence Against the Dark Arts(1991-1992))|(Defence Against the Dark Arts(1992-1993))|(Headmistress of Beauxbatons Academy of Magic)|(Caretaker of Hogwarts)|(Matron at Hogwarts School)|(Flying Instructor at Hogwarts)|(Librarian at Hogwarts)|(Astronomer at Hogwarts)')== False]
students2 = df[df['Job'].isna()]
students_and_muggles = pd.concat([students1, students2], axis=0)
muggles = df[df['Name'].str.match('.*(Dursley)')== True]
students = students_and_muggles[(students_and_muggles["Id"] != 120) & (students_and_muggles["Id"] != 121) & (students_and_muggles["Id"] != 122) & (students_and_muggles["Id"] != 123)]

