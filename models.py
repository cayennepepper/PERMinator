from server import db
from datetime import datetime
from sqlalchemy import ForeignKey

def serialize_timedelta(time_object):
  return str(time_object.days)+":"+str(time_object.seconds)

def serialize_permtime(date_time):
  d = str(date_time.day);
  m = str(date_time.month);
  y = str(date_time.year);
  return m + "/" + d + "/" + y

class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=False)
  sFirstName = db.Column(db.String(50))
  sLastName = db.Column(db.String(50))
  year = db.Column(db.Integer)
  college = db.Column(db.String(6))
  sEmail = db.Column(db.String(50))

  def __init__(self, id, sFirstName, sLastName, year, college, sEmail):
    self.id = id
    self.sFirstName = sFirstName
    self.sLastName = sLastName
    self.year = year
    self.college = college
    self.sEmail = sEmail
    
  def __repr__(self):
    return "<Student(id='%s', sFirstName='%s', sLastName='%s', year='%s', college='%s', sEmail='%s')>" % (
      self.id, self.sFirstName, self.sLastName, self.year, self.college,self.sEmail)

  #ignore_id is a boolean. true if we don't want to serialize the id
  def serialize(self, ignore_id=False): #lets us serialize it!!
    result = {}
    for key in self.__mapper__.c.keys():
      if (not ignore_id or key!="id"):
        result[key] = getattr(self,key)
    return result

class Course(db.Model):
  #reference sections via 'sections'
  id = db.Column(db.String(20), primary_key=True, autoincrement=False)

  def __init__(self, id):
    self.id = id

  def __repr__(self):
    return "<Course(courseID='%s')>" % (self.id)

class Section(db.Model):
  #reference PERMs via 'PERMs', teach table via 'taught_by'
  id = db.Column(db.Integer, primary_key=True, autoincrement=False)
  sectionNum = db.Column(db.Integer)
  courseID = db.Column(db.String(20), ForeignKey(Course.id))

  #reference course via 'course'
  course = db.relationship("Course", backref=db.backref('sections', order_by=sectionNum))

  def __init__(self,course, sectionNum,id):
    self.courseID = course
    self.sectionNum = sectionNum
    self.id = id

  def __repr__(self):
    return "<Section(sectionID='%s', courseID='%s', sectionNum ='%s')>" % (
      self.id, self.courseID, self.sectionNum)

  def serialize(self): #lets us serialize it!!
    result = {}
    for key in self.__mapper__.c.keys():
        result[key] = getattr(self,key)
    return result

class PERM(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  blurb = db.Column(db.String(200))
  status = db.Column(db.Enum("Expired", "Approved", "Denied", "Cancelled", "Requested"))
  submissionTime = db.Column(db.DateTime)
  expirationTime = db.Column(db.DateTime)
  sectionRank = db.Column(db.Integer)

  showBlurb = False

  studentID = db.Column(db.Integer, ForeignKey(Student.id), primary_key=True, autoincrement=False)
  #reference student via 'student'
  student= db.relationship("Student", backref=db.backref('PERMs', order_by=submissionTime))
  sectionID = db.Column(db.Integer, ForeignKey(Section.id), primary_key=True, autoincrement=False)
  #reference section via 'section'
  section = db.relationship("Section", backref=db.backref('PERMs', order_by=studentID))

  def __init__(self,section,student,blurb,status,submissionTime,expirationTime,sectionRank):
    self.sectionID = section
    self.studentID = student
    self.blurb = blurb
    self.status = status
    self.submissionTime = submissionTime
    self.expirationTime = expirationTime
    self.sectionRank = sectionRank

  def __repr__(self):
    return "<PERM(id='%s', section='%s', student='%s', blurb='%s', status='%s', submissionTime='%s', expirationTime='%s', sectionRank='%s')>" % (
      self.id, self.sectionID, self.studentID, self.blurb, self.status, self.submissionTime, self.expirationTime, self.sectionRank)

  def serialize(self): #lets us serialize it!!
    result = {}
    for key in self.__mapper__.c.keys():
      k = getattr(self,key)
      if( isinstance(k,datetime) ) :
        result[key] = serialize_permtime(k)
      else :
        result[key] = getattr(self,key)
    return result

class Professor(db.Model):
  #reference teach via 'teaches'
  id = db.Column(db.Integer, primary_key=True, autoincrement=False)
  pFirstName = db.Column(db.String(50))
  pLastName = db.Column(db.String(50))

  def __init__(self, profID, pFirstName, pLastName):
    self.id = profID
    self.pFirstName = pFirstName
    self.pLastName = pLastName

  def __repr__(self):
    return "<Professor(profID='%s', FirstName='%s', LastName='%s')>" % (self.id, self.pFirstName, self.pLastName)

class Teach(db.Model):
  profID = db.Column(db.Integer, ForeignKey(Professor.id), primary_key=True, autoincrement=False)
  sectionID = db.Column(db.Integer, ForeignKey(Section.id), primary_key=True,autoincrement=False)
  #reference section via 'section'
  section = db.relationship("Section", backref=db.backref('taught_by', order_by=profID))
  #reference prof via 'prof'
  prof = db.relationship("Professor", backref=db.backref('teaches', order_by=sectionID))

  def __init__(self, profID, sectionID):
    self.profID = profID
    self.sectionID = sectionID

  def __repr__(self):
    return "<Teach(profID='%s', sectionID='%s')>" % (self.profID, self.sectionID)

class Major(db.Model):
  #reference majorsIn students via 'students_in'
  id = db.Column(db.Integer, primary_key=True)
  college = db.Column(db.Enum("HMC", "CMC", "Pomona", "Pitzer", "Scripps"))
  name = db.Column(db.String(50))

  def __init__(self, college, name):
    self.college = college
    self.name = name

  def __repr__(self):
    return "<Major(college='%s', name='%s')>" % (self.college, self.name)

  def serialize(self, i=0): #lets us serialize it!!
    result = {}
    for key in self.__mapper__.c.keys():
        result["major" + key + str(i)] = getattr(self,key)
    return result

  def serializeString(self,i=0):
    result = ""
    for key in self.__mapper__.c.keys():
        if(key == "name") :
          result = result + " " + str(getattr(self,key))
        if(key == "college") :
          result = result + "MAJ_DIV"
    return str(getattr(self,"name")) + " (" + str(getattr(self,"college")) + ")";
  
class MajorsIn(db.Model):
  majorID = db.Column(db.Integer, ForeignKey(Major.id), primary_key=True, autoincrement=False)
  #reference major via 'major'
  major = db.relationship("Major", backref=db.backref('students_in'))
  studentID = db.Column(db.Integer, ForeignKey(Student.id), primary_key=True, autoincrement=False)
  #reference student via 'student'
  student = db.relationship("Student", backref=db.backref('majors_in'))

  def __init__(self, majorID,studentID):
    self.majorID = majorID
    self.studentID = studentID

  def __repr__(self):
    return "<MajorsIn(studentID='%s', majorID='%s')>" % (self.studentID, self.majorID)

class SatisfiesMajor(db.Model):
  #reference PERMs via 'PERMs', teach table via 'taught_by'
  majorID = db.Column(db.Integer, ForeignKey(Major.id), primary_key=True, autoincrement=False)
  courseID = db.Column(db.String(20),ForeignKey(Course.id),  primary_key=True, autoincrement=False)

  #reference course via 'course'
  major = db.relationship("Major", backref=db.backref('satisfied_by'))
  course = db.relationship("Course", backref=db.backref('satisfies'))

  def __init__(self,majorID, courseID):
    self.majorID = majorID
    self.courseID = courseID

  def __repr__(self):
    return "<SatisfiesMajor(majorID='%s', courseID='%s')>" % (self.majorID, self.courseID)

class HasTaken(db.Model):
  courseID = db.Column(db.String(20), ForeignKey(Course.id), primary_key=True, autoincrement=False)
  #reference major via 'major'
  course = db.relationship("Course", backref=db.backref('taken_by'))
  studentID = db.Column(db.Integer, ForeignKey(Student.id), primary_key=True, autoincrement=False)
  #reference student via 'student'
  student = db.relationship("Student", backref=db.backref('courses_taken', order_by=courseID))

  def __init__(self, courseID,studentID):
    self.courseID = courseID
    self.studentID = studentID

  def __repr__(self):
    return "<HasTaken(studentID='%s', courseID='%s')>" % (self.studentID, self.courseID)