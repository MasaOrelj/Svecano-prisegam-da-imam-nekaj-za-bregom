from bottleext import *

@route('hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

debug(True)
run(host='localhost', port=8085)

