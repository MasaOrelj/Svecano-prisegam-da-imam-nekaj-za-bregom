#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user, debug
import bottle

from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import os

repo = Repo()
auth = AuthService(repo)

SERVER_PORT = os.environ.get('BOTTLE_PORT', 8081)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

@bottle.get('/prijava/')
def prijava_get():
    return template_user('prijava.html', napaka=None)

@bottle.post('/prijava/')
def prijava_post():
    #uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    #geslo_v_cistopisu = bottle.request.forms.getunicode('geslo')
    #if not uporabnisko_ime:
    #    return bottle.template('registracija.html', napaka="Vnesi uporabniško ime!")
    #try:  
        #Uporabnik.prijava(uporabnisko_ime, geslo_v_cistopisu)
        #bottle.response.set_cookie(PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST)
        bottle.redirect('/')
    #except ValueError as e:
    #    return bottle.template("prijava.html", napaka=e.args[0])

@bottle.post('/odjava/')
def odjava():
    #bottle.response.delete_cookie(PISKOTEK_UPORABNISKO_IME, path='/')
    bottle.redirect('/')

@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napaka=None)

@bottle.post("/registracija/")
def registracija_post():
    #uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    #geslo_v_cistopisu = bottle.request.forms.getunicode("geslo")
    #if not uporabnisko_ime:
    #    return bottle.template("registracija.html", napaka="Vnesi uporabniško ime!")
    #try:
    #    Uporabnik.registracija(uporabnisko_ime, geslo_v_cistopisu)
    #    bottle.response.set_cookie(
    #        PISKOTEK_UPORABNISKO_IME, uporabnisko_ime, path="/", secret=SKRIVNOST
    #    )
        bottle.redirect("/")
    #except ValueError as e:
    #    return bottle.template(
    #        "registracija.html", napaka=e.args[0]
    #    )

@bottle.get('/')
def osnovna_stran():
    return bottle.template('osnovna_stran.html')

@bottle.get('/profile/')
def houses_get():
    return bottle.template("profile.html") 

@bottle.post('/profile/')
def houses_get():
    bottle.redirect('/') 
 
@bottle.get('/house/')
def houses_get():
    return bottle.template("house.html") 

@bottle.post('/house/')
def houses_get():
    bottle.redirect('/')   


@bottle.get('/subjects/')
def houses_get():
    return bottle.template("house.html") 

@bottle.post('/subjects/')
def houses_get():
    bottle.redirect('/')   

@bottle.get('/forum/')
def houses_get():
    return bottle.template("forum.html") 

@bottle.post('/forum/')
def houses_get():
    bottle.redirect('/')
    

debug(True)

 
# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)