# rezervacije: bere, ureja, briše, naredi novo r
# registracija gosta 
# registracija receptorja --> vidi vse rezervacije: lahko glede na dan začetka rezervacin 
# in glede na dan zacetek + stevilo nočitev
from datetime import datetime as dt, timedelta
# uvozimo psycopg2
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

from typing import List, TypeVar, Type, Callable
from Data.Modeli import *    #uvozimo classe tabel

#from pandas import DataFrame
#from re import sub

import Data.auth as auth  
from datetime import date
import random


class Repo:

    def __init__(self):
        self.conn = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password, port=5432)
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    
    def tabela_student(self) -> List[Student]:
        self.cur.execute("""
            SELECT * FROM student
        """)
        return [Student(id, name, username, password, patronus, house_id) for (id, name, username, password, patronus, house_id) in self.cur.fetchall()]

    def dodaj_student(self, Student: Student) -> Student:
        # ali je že v tabeli?
        self.cur.execute("""
            SELECT * from student
            WHERE "Username" = %s
            """, (Student.username,))
        row = self.cur.fetchone()
        if row:
            Student.id = row[0]
            return Student
        #nov uporabnik
        self.cur.execute("""
            INSERT INTO student ("Name", "Username", "Password", "Patronus", "House_id")
             VALUES (%s, %s, %s, %s, %s); """, (Student.name, Student.username, Student.password, Student.patronus, Student.house_id))
        self.conn.commit()
        id_predmetov = [1,2,3,4,11,7,8,12,13,14,38,39,43,46,47,49,54,55,58,48,10]
        randomlist = random.sample(id_predmetov, 5)
        self.cur.execute("""SELECT * FROM Student WHERE "Username" = %s""", [Student.username])
        lst = self.cur.fetchall()[0]
        student_id = lst[0]
        for i in range (0,5):
            self.cur.execute(""" INSERT INTO student_subject ("student_id", "subject_id") VALUES (%s,%s);""", (student_id, randomlist[i]))
        self.conn.commit()
        return Student
    
    def dodaj_post(self, Post: Post) -> Post:
        self.cur.execute("""
            INSERT INTO post ("text")
             VALUES (%s); """, (Post.post))
        self.conn.commit()
        return Student
    
