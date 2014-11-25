""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)
from flask.ext.sqlalchemy import SQLAlchemy
from models import *
import re
from datetime import datetime

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
    perm_set = db.session.query(PERM).join(Section).filter(Section.courseID==cid).all()
    perms = [perm.serialize() for perm in perm_set]
    return render_template('prof_perms.html', perms=perms)

@app.route('/student/<string:sid>')
def student_home(sid):
    student_perms = db.session.query(PERM).filter(PERM.studentID==sid).all()
    student_perms = [studentperm.serialize() for studentperm in student_perms]
    return render_template('studentHome.html', studentperms=student_perms)

@app.route('/perms/', methods=['POST'])
def studentperm_create():
    st_perm = request.get_json()
    print st_perm
    db.session.add(PERM(section=int(st_perm[u'sectionId']), student=45, blurb=st_perm[u'blurb'], status='REQUESTED', submissionTime=datetime.now(), expirationTime=datetime.now(), sectionRank=1))
    db.session.commit()
    return "Good"

@app.route('/perms/<string:pid>', methods=['PUT', 'PATCH'])
def perm_update(pid):
    new_item = request.get_json()
    #get the datetime from the string
    new_exp_time = re.match("(\d?\d)/(\d?\d)((/(\d\d\d?\d?))?)", new_item[u'expirationTime'])
    if new_exp_time!=None:
        new_year = new_exp_time.group(5)
        if (new_year!=None):
            new_year = int(new_year)
            if (new_year<2000):
                new_year = new_year+2000
        else:
            new_year = datetime.now().year
        new_exp_datetime = datetime(new_year, int(new_exp_time.group(1)), int(new_exp_time.group(2)))
        db.session.query(PERM).filter(PERM.id==pid).update({
        PERM.status:new_item[u'status'], 
        PERM.expirationTime:new_exp_datetime, 
        PERM.sectionRank:new_item[u'sectionRank'], 
        PERM.blurb:new_item[u'blurb']
        })
        db.session.commit()
        return "Fine"
    else:
        return "Invalid Expiration Date", 409
    
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
