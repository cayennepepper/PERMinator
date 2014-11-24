""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)
from flask.ext.sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__, static_url_path='')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0'
db = SQLAlchemy(app)

@app.route('/professor/<int:pid>/sections')
def prof_home(pid):
    prof_teach = db.session.query(Teach).filter(Teach.profID==pid).all()
    sections = [teach.section.serialize() for teach in prof_teach]
    return render_template('prof_home.html', sections=sections)

@app.route('/course/<string:cid>')
def prof_perms(cid):
    perm_set = db.session.query(Section).join(PERM).filter(Section.courseID==cid).all()
    perms = [perm.serialize() for perm in perm_set]
    return render_template('prof_perms.html', perms=perms)

@app.route('/')
def index():
    todos = db.session.query(Item).all()
    _todos = [todo.serialize() for todo in todos if todo!=None]
    return render_template('index.html', todos=_todos)


@app.route('/todos/', methods=['POST'])
def todo_create():
    todo = request.get_json()
    db.session.add(Item(todo))
    db.session.commit()
    return "Good"


@app.route('/todos/<int:id>')
def todo_read(id):
    todo = db.session.query(Item).filter(Item.id==id).first()
    if todo==None:
        abort(404) #send error message
    return jsonify(todo.serialize())


@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
def todo_update(id):
    new_item = request.get_json()
    print request.get_json
    print new_item[u'title']
    db.session.query(Item).filter(Item.id==id).update({Item.title:new_item[u'title']})
    print "NEW IN DB:", db.session.query(Item).filter(Item.id==id).all()
    db.session.commit()
    return "Fine"


@app.route('/todos/<int:id>', methods=['DELETE'])
def todo_delete(id):
    db.session.query(Item).filter(Item.id==id).delete()
    db.session.commit()
    return "Fine"

if __name__ == '__main__':
    app.run(port=8000)
