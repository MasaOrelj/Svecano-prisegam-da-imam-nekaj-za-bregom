import os
import bottle
from bottle import *


class Route(bottle.Route):
    """
    Nadomestni razred za poti s privzetimi imeni.
    """
    def __init__(self, app, rule, method, callback, name=None, plugins=None, skiplist=None, **config):
        if name is None:
            name = callback.__name__
        def decorator(*largs, **kwargs):
            bottle.request.environ['SCRIPT_NAME'] = os.environ.get('BOTTLE_ROOT', '')
            return callback(*largs, **kwargs)
        super().__init__(app, rule, method, decorator, name, plugins, skiplist, **config)


def template(*largs, **kwargs):
    """
    Izpis predloge s podajanjem funkcije url.
    """

    
    return bottle.template(*largs, **kwargs, url=bottle.url)

def template_user(*largs, **kwargs):
    """
    Izpis predloge s podajanjem funkcije url in dodanim uporabnikom ter njegovo.
    """
    # Dodamo ime uporabnika, ki je prebran iz cookija direktno v vsak html, ki ga uporabimo kot template.
    usr_cookie = request.get_cookie("uporabnik")
    usr_role = request.get_cookie("rola")
    return bottle.template(*largs, **kwargs, uporabnik=usr_cookie, rola=usr_role, url=bottle.url)



bottle.Route = Route