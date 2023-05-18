#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import *

from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import Data.auth as auth_public
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os

repo = Repo()
auth = AuthService(repo)

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8081)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

@get('/')
def osnovna_stran():
    return bottle.template('osnovna_stran.html')

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
        cur.execute("SELECT geslo FROM student WHERE username = %s", [uporabnisko_ime])
        hashBaza = cur.fetchall()[0][0]
        cur.execute("SELECT id FROM uporabnik WHERE username = %s", [uporabnisko_ime])
        id_gosta = cur.fetchall()[0][0]
    except:
        hashBaza = None
    if hashBaza is None:
        redirect(url('prijava_get'))
        return
    if geslo != hashBaza:
         redirect(url('prijava_get'))
         return
    redirect(url('osnovna_stran', id_gosta=id_gosta))

@get('/odjava')
def odjava():
    response.delete_cookie("uporabnik")
    response.delete_cookie("rola")
    return template('osnova_stran.html', napaka=None)


conn = psycopg2.connect(database=auth_public.db, host=auth_public.host, user=auth_public.user, password=auth_public.password, port=DB_PORT)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor) 

debug(True)

# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)