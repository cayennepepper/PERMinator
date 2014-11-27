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
    perms = []

    perm_set = db.session.query(PERM).join(Section).filter(Section.courseID==cid).join(Student).filter(Student.id == PERM.studentID).all()
    for p in perm_set :
        m = {}
        for i in range(len(p.student.majors_in)) :
            m = dict(m.items() + p.student.majors_in[i].major.serialize(i).items())
        print m
        perms = [dict(p.serialize().items() + p.student.serialize(True).items() + m.items()) for p in perm_set]
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
    db.session.add(PERM(section=int(st_perm[u'sectionId']), student=10234873, blurb=st_perm[u'blurb'], status='REQUESTED', submissionTime=datetime.now(), expirationTime=datetime.now(), sectionRank=1))
    db.session.commit()
    return "Good"

@app.route('/perms/<string:pid>', methods=['PUT', 'PATCH'])
def perm_update(pid):
    new_item = request.get_json()
    print "updating"
    #get the datetime from the string
    new_exp_time = re.match("(\d?\d)/(\d?\d)((/(\d\d\d?\d?))?)", new_item[u'expirationTime'])
    if new_exp_time!=None:
        new_year = new_exp_time.group(5)
        if (new_year!=None):
            new_year = int(new_year)
            if (new_year<100):
                new_year = new_year+2000
        else:
            new_year = datetime.now().year
        new_exp_datetime = datetime(new_year, int(new_exp_time.group(1)), int(new_exp_time.group(2)))
        print new_exp_datetime
        db.session.query(PERM).filter(PERM.id==pid).update({
        PERM.status:new_item[u'status'], 
        PERM.expirationTime:new_exp_datetime, 
        PERM.sectionRank:new_item[u'sectionRank'], 
        PERM.blurb:new_item[u'`blurb']
        })
        db.session.commit()
        print "new:", db.session.query(PERM).filter(PERM.id==pid).all()
        return "Fine"
    else:
        return "Invalid Expiration Date", 409


if __name__ == '__main__':
    app.run(port=8000)
