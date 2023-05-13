
from Data.Database import Repo
from Data.Modeli import *
from typing import Dict
from re import sub
import dataclasses
import bcrypt
from typing import Type
from datetime import date

class AuthService:

    repo : Repo
    def __init__(self, repo : Repo):
        
        self.repo = repo

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            user = self.repo.dobi_gen_id(Student, uporabnik, id_col="username")
            return True
        except:
            return False

    def prijavi_uporabnika(self, uporabnik : str, geslo: str) -> StudentDTO | bool :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_gen_id(Student, uporabnik, id_col="username")

        geslo_bytes = geslo.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_bytes, user.password_hash.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.last_login = date.today().isoformat()
            self.repo.posodobi_gen(user, id_col="username")
            return StudentDTO(username=user.username, role=user.role)
        
        return False

    def dodaj_uporabnika(self, uporabnik: str, rola: str, geslo: str) -> StudentDTO:

        # zgradimo hash za geslo od uporabnika

        # Najprej geslo zakodiramo kot seznam bajtov
        bytes = geslo.encode('utf-8')
  
        # Nato ustvarimo salt
        salt = bcrypt.gensalt()
        
        # In na koncu ustvarimo hash gesla
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Student in ga zapišemo bazo

        uporabnik = Student(
            username=uporabnik,
            role=rola,
            password_hash=password_hash.decode(),
            last_login= date.today().isoformat()
        )

        self.repo.dodaj_gen(uporabnik, serial_col=None)

        return StudentDTO(username=uporabnik, role=rola)