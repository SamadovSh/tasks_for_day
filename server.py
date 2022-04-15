from bottle import route, run, view, static_file, redirect, request
from db import TodoItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
s = Session()


@route('/')
@view('index')
def index():
    tasks = s.query(TodoItem).order_by(TodoItem.uid)
    return {'tasks': tasks}


@route('/static/<filename:path>')
def send_static(filename):
    return static_file(filename, root='static')


@route('/add-task', method="POST")
def add_task():
    desc = request.POST.description.strip()
    if len(desc) > 0:
        t = TodoItem(desc)
        s.add(t)
        s.commit()
    return redirect('/')


@route('/api/delete/<uid:int>')
def api_delete(uid):
    s.query(TodoItem).filter(TodoItem.uid == uid).delete()
    s.commit()
    return redirect('/')


@route('/api/complete/<uid:int>')
def api_complete(uid):
    t = s.query(TodoItem).filter(TodoItem.uid == uid).first()
    t.is_completed = True
    s.commit()
    return 'OK'


if os.environ.get('APP_LOCATION') == 'heroku':
    run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
else:
    run(host='localhost', port='8080')
