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

    #404 redirect
    if(len(prof_teach) == 0) :
        return render_template('four_oh_four.html'), 404

    sections = [teach.section.serialize() for teach in prof_teach]
    return render_template('prof_home.html', sections=sections, name=db.session.query(Professor).get(pid).pFirstName)

@app.route('/section/<string:secid>')
def prof_perms(secid):
    this_section = db.session.query(Section).get(secid)

    #404 redirect
    if(this_section is None) :
        return render_template('four_oh_four.html'), 404
        
    this_section_num = this_section.sectionNum
    this_course_id = this_section.courseID
    perms = []

    perm_set = db.session.query(PERM).filter(PERM.status!="Cancelled").filter(PERM.sectionID==secid).join(Student).filter(Student.id == PERM.studentID).all()
    if (len(perm_set)==0):
        return render_template("prof_perms_empty.html", courseID = this_course_id, sectionNum = this_section_num)
    

    mMap = {}
    satMap = {}
    sections = db.session.query(Section).get(secid).course.sections
    student_sections = {}
    prev_courses = {}
    for p in perm_set :
        student_perms = []
        for section in sections:
            this_student = p.student.id
            student_perms.append((section.sectionNum, db.session.query(PERM).filter(PERM.sectionID==section.id).filter(PERM.status!="Cancelled").filter(PERM.studentID==this_student).first()))       
        prev_courses[str(p.id)] = [hasTaken.courseID for hasTaken in p.student.courses_taken]
        m = ""
        satisfiesMajor = []
        for i in range(len(p.student.majors_in)) :
            maj = p.student.majors_in[i].major
            m = m + str(maj.serializeString(i)) + "MAJ_DIV"
            satisfiesMajor = satisfiesMajor+[True for satisfiesMajor in maj.satisfied_by if satisfiesMajor.courseID==this_course_id]
        mMap[str(p.id)] = m
        satMap[str(p.id)] = satisfiesMajor
        student_sections[str(p.id)]= {sectionNum:perm.serialize() for (sectionNum, perm) in student_perms if perm!=None}
    perms = [dict(p.serialize().items() + p.student.serialize(True).items() + {"totalSections":len(sections)}.items() + {"majors":mMap[str(p.id)]}.items() +{"courseHistory":prev_courses[str(p.id)]}.items() + {"satisfiesMaj":(len(satMap[str(p.id)])!=0)}.items() + {"perms":student_sections[str(p.id)]}.items()) for p in perm_set]
    return render_template('prof_perms.html', perms=perms, courseID = this_course_id, sectionNum = this_section_num)


@app.route('/student/<string:sid>')
def student_home(sid):
    #404 redirect
    student = db.session.query(Student).filter(Student.id==sid).first()
    if(student is None) :
        return render_template('four_oh_four.html'), 404
    student_perms = db.session.query(PERM).filter(PERM.studentID==sid).all()
    student_perms = [studentperm.serialize() for studentperm in student_perms]

    new_student_perms = []
    for studentperm in student_perms:
        #Get the course id and section number
        db_section_pre = db.session.query(Section).filter(Section.id==studentperm['sectionID'])
        db_section_id_q = db_section_pre.first()
        db.session.commit()

        db_section_num = db_section_id_q.serialize()['sectionNum']
        db_section_course_id = db_section_id_q.serialize()['courseID']

        #Set course id in student perms, sectionNum
        studentperm['course'] = db_section_course_id
        studentperm['sectionNum'] = db_section_num

    return render_template('studentHome.html', studentperms=student_perms, sid = sid, name=student.sFirstName)

@app.route('/perms/', methods=['POST'])
def studentperm_create():
    st_perm = request.get_json()
    #Find section id based on given course
    db_section = db.session.query(Section).filter(Section.sectionNum==st_perm[u'sectionNum'], Section.courseID==st_perm[u'course']).first()
    if (db_section==None):
        return "Invalid Course "+st_perm[u'course']+"-"+st_perm[u'sectionNum']+". This PERM will not be saved.", 409

    db_existing_perms = db.session.query(PERM).filter(PERM.sectionID == db_section.id, PERM.studentID==st_perm[u'studentID'] ).all()
    for existing in db_existing_perms :
        if(existing.status != "Cancelled"):
            return "You already have a PERM for this section. This PERM will not be saved.", 409

    db_other_perms = db.session.query(PERM).filter(PERM.studentID==st_perm[u'studentID']).join(Section).filter(Section.id == PERM.sectionID).filter(Section.courseID==st_perm[u'course']).all()
    for other in db_other_perms :
        if(int(other.sectionRank) == int(st_perm[u'sectionRank']) and other.status != "Cancelled"):
            return "You already have a PERM with this ranking. Please choose a different ranking. This PERM will not be saved otherwise.", 409


    db_section_id = db_section.id
    section_rank = st_perm[u'sectionRank']
    #Create exp date 2 weeks from now
    now_time = datetime.now()
    future_time = now_time + timedelta(days=14)

    db.session.add(PERM(section=db_section_id, student=st_perm[u'studentID'], blurb=st_perm[u'blurb'], status=st_perm[u'status'], submissionTime=now_time, expirationTime=future_time, sectionRank=section_rank))
    db.session.commit()
    perm = db.session.query(PERM).filter(PERM.sectionID==db_section_id, PERM.studentID==st_perm[u'studentID']).first()
    return jsonify(perm.serialize())

@app.route('/perms/<string:pid>', methods=['PUT', 'PATCH'])
def perm_update(pid):
    new_item = request.get_json()

    if(new_item[u'status'] != "Cancelled") :
        if u'course' in new_item.keys():
            db_other_perms = db.session.query(PERM).filter(PERM.studentID==new_item[u'studentID']).join(Section).filter(Section.id == PERM.sectionID).filter(Section.courseID==new_item[u'course']).all()
            for other in db_other_perms :
                if(int(other.sectionRank) == int(new_item[u'sectionRank']) and other.status != "Cancelled" and int(other.id) != int(pid)):
                    return "You already have a PERM with this ranking. Please choose a different ranking.", 409

    #get the datetime from the string
    new_status = new_item[u'status']
    if new_status=="Approved" or new_status=="Requested": #only check for a valid expiration date if we care
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
                return "Past Expiration Date. Please choose an expiration in the future.", 409
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
            return "Invalid Expiration Date. Please input in the format dd/mm/yyyy.", 409
    else:
        db.session.query(PERM).filter(PERM.id==pid).update({
                PERM.status:new_item[u'status'], 
                PERM.sectionRank:new_item[u'sectionRank'], 
                PERM.blurb:new_item[u'blurb']
                })
        db.session.commit()
        return "Fine!"

@app.errorhandler(404)
def page_not_found(e):
    return render_template('four_oh_four.html'), 404


if __name__ == '__main__':
    app.run(port=8000)
