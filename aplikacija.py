from bottleext import *

from database import Repo
from Data.Modeli import *
from Data.Services import AuthService
from functools import wraps

import Data.auth_public as auth_public
import psycopg2, psycopg2.extensions, psycopg2.extras
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE) # se znebimo problemov s šumniki

import os
import csv
import random

repo = Repo()

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
        return template('prijava.html')
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
        hashBaza = cur.execute('SELECT "Password" FROM student WHERE "Username" = %s', [uporabnisko_ime])
        hashBaza = cur.fetchone()[0]
        id_studenta = cur.execute('SELECT "id" FROM student WHERE "Username" = %s', [uporabnisko_ime])
        id_studenta = cur.fetchall()[0]
    except:
        hashBaza = None
    if hashBaza is None:
        redirect(url('prijava_get'))
        return
    if geslo != hashBaza:
         redirect(url('prijava_get'))
         return
    response.set_cookie("username", uporabnisko_ime,  path = "/") #secret = "secret_value",, httponly = True)
    #response.set_cookie("rola", "receptor",  path = "/")
    redirect(url('profile_get', id_studenta=id_studenta))

@get('/odjava')
def odjava():
    response.delete_cookie("username")
    response.delete_cookie("password")
    return template('osnovna_stran.html', napaka=None)

@get('/registracija')
def registracija_get():
    return template('registracija.html')

    
def dodaj_house(question1, question2, question3, question4, question5):
    house_scores = {
        'gryffindor': 0,
        'hufflepuff': 0,
        'ravenclaw': 0,
        'slytherin': 0
    }

    #glede na odgovore (njihove vrednosti) prišteje točke
    house_scores[question1] += 1
    house_scores[question2] += 1
    house_scores[question3] += 1
    house_scores[question4] += 1
    house_scores[question5] += 1

    #pogleda, kateri ma najvišji score
    max_score = max(house_scores.values())
    houses_with_max_score = [house for house, score in house_scores.items() if score == max_score]
    house = houses_with_max_score[0]  #če je isto točk izbere prvo
    if house == 'gryffindor':
        house = [house,1]
    elif house == 'hufflepuff':
        house = [house,2]
    elif house == 'ravenclaw':
        house = [house,3]
    elif house == 'slytherin':
        house = [house,4]

    return house[1]


#random izbira živali za patronus
animals = []
with open('Animals.csv', 'r') as file:
    reader = csv.reader(file)
    for row in reader:
        animals.append(row[0])

@post('/registracija')
def registracija_post():
    name = request.forms.name
    username = request.forms.username
    password = request.forms.password
    patronus = random.choice(animals)
    question1 = request.forms.get('question1')
    question2 = request.forms.get('question2')
    question3 = request.forms.get('question3')
    question4 = request.forms.get('question4')
    question5 = request.forms.get('question5')
    house_id = dodaj_house(question1, question2, question3, question4, question5)
    student1=Student(name=name, house_id=house_id, patronus=patronus, username=username, password=password)
    repo.dodaj_student(student1)
    redirect(url('osnovna_stran'))

@get('/profile')
@cookie_required
def profile_get():
    uporabnik = request.get_cookie("username")
    # id_gosta = int(request.cookies.get("id"))
    cur.execute("""SELECT * FROM Student WHERE "Username" = %s""", [uporabnik])
    lst = cur.fetchall()[0]
    id = lst[0]
    name = str(lst[1])
    house = int(lst[2])
    patronus = str(lst[3])
    username = str(lst[4])
    password = str(lst[5])
    return template("profile.html", id=id, name=name, house=house, patronus=patronus, username=username, password=password) #Preko tega do spremeljivk

@post('/profile')
def profile_post():
    redirect(url('osnovna_stran'))
 
@get('/forum')
def post_get():
    cur.execute(""" SELECT * FROM post """)
    posts = cur.fetchall() #dobi vse objave
    comments = {}
    cur.execute("SELECT post_id, text FROM comment")
    all_comments = cur.fetchall()
    for comment in all_comments:
        post_id, text = comment
        if post_id in comments:
            comments[post_id].append(text)
        else:
            comments[post_id] = [text]
    return template('forum.html', posts=posts, comments=comments)

@post('/forum')
@cookie_required
def forum_post():
    uporabnik = request.get_cookie("username")
    cur.execute("""SELECT * FROM Student WHERE "Username" = %s""", [uporabnik])
    lst = cur.fetchall()[0]
    id_user = lst[0]
    username = str(lst[4])
    likes = 1
    content = request.forms.get('content')
    cur.execute(""" INSERT INTO post ("text", "likes", "student_id") 
                    VALUES (%s, %s, %s)""", (content, likes, id_user))
    conn.commit()
    redirect(url('post_get'))
    
@post('/comment/<post_id:int>')
@cookie_required
def comment_post(post_id: str):
    uporabnik = request.get_cookie("username")
    cur.execute("""SELECT * FROM Student WHERE "Username" = %s""", [uporabnik])
    lst = cur.fetchall()[0]
    id_user = lst[0]
    username = str(lst[4])
    content_comment = request.forms.get('content')
    cur.execute(""" INSERT INTO comment ("text", "student_id", "post_id") 
                    VALUES (%s, %s, %s)""", (content_comment, id_user, int(post_id)))
    conn.commit()
    redirect(url('post_get'))

@get('/house')
def houses_get():
    return template("house.html") 

@post('/house')
def houses_post():
    redirect(url('osnovna_stran'))  

@get('/subjects')
def subjects_get():
    return template("subjects.html") 

@post('/subjects')
def subjects_post():
    redirect(url('osnovna_stran'))  


@get('/professors')
def professors_get():
    return template("professors.html") 

@post('/professors')
def professors_post():
    redirect(url('osnovna_stran'))

static_dir = "./images"

@route("/images/<filename:path>") 
def static(filename):
    return static_file(filename, root=static_dir)

debug(True)

if __name__ == "__main__":
    run(host='localhost', port=SERVER_PORT, reloader=RELOADER)
