#!/usr/bin/python
# -*- encoding: utf-8 -*-

# uvozimo bottle.py
from bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user, debug


from Data.Database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import os

repo = Repo()
auth = AuthService(repo)


# uvozimo ustrezne podatke za povezavo



import os

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)
DB_PORT = os.environ.get('POSTGRES_PORT', 5432)

# odkomentiraj, če želiš sporočila o napakah
# debug(True)



@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')



@get('/')
def index():
    """
    Domača stran je stran z cenami izdelkov.
    """
        
    return template_user('profil.html')
 
    

debug(True)

 
# poženemo strežnik na podanih vratih, npr. http://localhost:8080/
if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)