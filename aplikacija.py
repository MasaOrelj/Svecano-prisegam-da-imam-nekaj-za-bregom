from bottleext import *

from database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import Data.auth as auth_public
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os

Repo = Repo()

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8081)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

conn = psycopg2.connect(database=auth_public.db, host=auth_public.host, user=auth_public.user, password=auth_public.password, port=DB_PORT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

@get('/')
def osnovna_stran():
    return template('osnovna_stran.html')

def cookie_required(f):
    """
    Dekorator, ki zahteva veljaven piškotek. Če piškotka ni, uporabnika preusmeri na stran za prijavo.
    """
    @wraps(f)
    def decorated( *args, **kwargs):
        cookie = request.get_cookie("username")
        if cookie:
            return f(*args, **kwargs)
        return template('subjects.html')
    return decorated

@get('/prijava') 
def prijava_get():
    return template("prijava.html")

@post('/prijava') 
def prijava_post():
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    if uporabnisko_ime is None or geslo is None:
        redirect(url('prijava_get'))
    hashBaza = None
    try: 
        hashBaza = cur.execute("SELECT Password FROM student WHERE Username = %s", [uporabnisko_ime])
        hashBaza = cur.fetchone()[0]
        id_studenta = cur.execute("SELECT id FROM student WHERE Username = %s", [uporabnisko_ime])
        id_studenta = cur.fetchall()[0]
        print('a')
    except:
        print("ne odcita hashBaze")
        hashBaza = None
    if hashBaza is None:
        redirect(url('prijava_get'))
        return
    if geslo != hashBaza:
         redirect(url('prijava_get'))
         return
    redirect(url('profile_get', id_studenta=id_studenta))

@get('/odjava')
def odjava():
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    return template('osnova_stran.html', napaka=None)

@get('/registracija')
def registracija_get():
    return template('registracija.html')

@post('/registracija')
def registracija_post():
    name = request.forms.name
    username = request.forms.username
    password = request.forms.password
    patronus = request.forms.patronus
    house_id = request.forms.house_id
    student1=Student(name=name, house_id=house_id, patronus=patronus, username=username, password=password)
    Repo.dodaj_student(student1)
    return 'Uspešna registracija'

@get('/profile')
def profile_get():
    return template("profile.html") 

@post('/profile')
def profile_post():
    redirect('/') 
 
@get('/house')
def houses_get():
    return template("house.html") 

@post('/house')
def houses_post():
    redirect('/')   

@get('/subjects')
def subjects_get():
    return template("subjects.html") 

@post('/subjects')
def subjects_post():
    redirect('/')   

@get('/forum')
def forum_get():
    return template("forum.html") 

@post('/forum')
def forum_post():
    redirect('/')


debug(True)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)