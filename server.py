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
from datetime import datetime, timedelta

app = Flask(__name__, static_url_path='')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0'
db = SQLAlchemy(app)

@app.route('/professor/<int:pid>/sections')
def prof_home(pid):
    prof_teach = db.session.query(Teach).filter(Teach.profID==pid).all()
    sections = [teach.section.serialize() for teach in prof_teach]
    return render_template('prof_home.html', sections=sections)

@app.route('/section/<string:secid>')
def prof_perms(secid):
    perms = []
    perm_set = db.session.query(PERM).filter(PERM.status!="Cancelled").filter(PERM.sectionID==secid).join(Student).filter(Student.id == PERM.studentID).all()
    mMap = {}
    sections = db.session.query(Section).get(secid).course.sections
    this_section_num = db.session.query(Section).get(secid).sectionNum
    student_sections = {}
    for p in perm_set :
        student_perms = []
        print student_perms
        for section in sections:
            this_student = p.student.id
            student_perms.append((section.sectionNum, db.session.query(PERM).filter(PERM.sectionID==section.id).filter(PERM.status!="Cancelled").filter(PERM.studentID==this_student).first()))
        m = ""
        for i in range(len(p.student.majors_in)) :
            m = m + str(p.student.majors_in[i].major.serializeString(i)) + "MAJ_DIV"
        mMap[str(p.id)] = m
        student_sections[str(p.id)]= [dict(perm.serialize().items()+{"sectionNum":sectionNum}.items()) for (sectionNum, perm) in student_perms if perm!=None]
        print student_sections
    perms = [dict(p.serialize().items() + p.student.serialize(True).items() + {"majors":mMap[str(p.id)]}.items() + {"perms":student_sections[str(p.id)]}.items() ) for p in perm_set]
    return render_template('prof_perms.html', perms=perms, courseID = sections[0].courseID, sectionNum = this_section_num)

@app.route('/student/<string:sid>')
def student_home(sid):
    student_perms = db.session.query(PERM).filter(PERM.studentID==sid).all()
    student_perms = [studentperm.serialize() for studentperm in student_perms]
    new_student_perms = []
    for studentperm in student_perms:
        #Get the course id
        db_section_id_q = db.session.query(Section).filter(Section.id==studentperm['sectionID']).first()
        db.session.commit()
        db_section_course_id = db_section_id_q.serialize()['courseID']
        #Set course id in student perms
        studentperm['course'] = db_section_course_id
    return render_template('studentHome.html', studentperms=student_perms)

@app.route('/perms/', methods=['POST'])
def studentperm_create():
    st_perm = request.get_json()
    #Find section id based on given course
    db_section_id_q = db.session.query(Section).filter(Section.sectionNum==st_perm[u'sectionID'], Section.courseID==st_perm[u'course']).first()
    db_section_id = int(db_section_id_q.serialize()['id'])

    section_rank = st_perm[u'sectionRank']

    db.session.add(PERM(section=db_section_id, student=123, blurb=st_perm[u'blurb'], status='REQUESTED', submissionTime=datetime.now(), expirationTime=datetime.now(), sectionRank=section_rank))
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
            if (new_year<100):
                new_year = new_year+2000
        else:
            new_year = datetime.now().year
        new_exp_datetime = datetime(new_year, int(new_exp_time.group(1)), int(new_exp_time.group(2)))
        if (datetime.now() - new_exp_datetime > timedelta(0)):
            return "ERROR: Past Expiration Date", 409
        else :
            db.session.query(PERM).filter(PERM.id==pid).update({
            PERM.status:new_item[u'status'], 
            PERM.expirationTime:new_exp_datetime, 
            PERM.sectionRank:new_item[u'sectionRank'], 
            PERM.blurb:new_item[u'blurb']
            })
            db.session.commit()
            return "success"
    else:
        return "ERROR: Invalid Expiration Date", 409


if __name__ == '__main__':
    app.run(port=8000)
