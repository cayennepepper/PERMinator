from server import db
from sqlalchemy import ForeignKey

#DB SCHEMA: STUDENT MODEL
class Student(db.Model):
  #reference PERMs via 'PERMs'
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

class Course(db.Model):
  #reference sections via 'sections'
  courseID = db.Column(db.String(20), primary_key=True, autoincrement=False)
  credits = db.Column(db.Numeric)

  def __init__(self, id, credits):
    self.courseID = id
    self.credits = credits

  def __repr__(self):
    return "<Course(courseID='%s', credits='%s')>" % (self.courseID, self.credits)

class Section(db.Model):
  #reference PERMs via 'PERMs', teach table via 'taught_by'
  sectionID = db.Column(db.Integer, primary_key=True, autoincrement=False)
  sectionNum = db.Column(db.Integer)
  enrollmentCap = db.Column(db.Integer)
  defaultExpiration = db.Column(db.Time)
  courseID = db.Column(db.String(20), ForeignKey(Course.courseID))

  #reference course via 'course'
  course = db.relationship("Course", backref=db.backref('sections', order_by=sectionNum))

  def __init__(self,cap,exp,course, sectionNum,id):
    self.enrollmentCap = cap
    self.defaultExpiration = exp
    self.courseID = course
    self.sectionNum = sectionNum
    self.sectionID = id

  def __repr__(self):
    return "<Section(sectionID='%s', enrollmentCap='%s', defaultExpiration='%s', courseID='%s', sectionNum ='%s')>" % (
      self.sectionID, self.enrollmentCap, self.defaultExpiration, self.courseID, self.sectionNum)

class PERM(db.Model):
  blurb = db.Column(db.String(200))
  status = db.Column(db.Enum("Revoked", "Approved", "Denied", "Cancelled", "Requested"))
  submissionTime = db.Column(db.DateTime)
  expirationTime = db.Column(db.DateTime)
  sectionRank = db.Column(db.Integer)

  studentID = db.Column(db.Integer, ForeignKey(Student.id), primary_key=True, autoincrement=False)
  #reference student via 'student'
  student= db.relationship("Student", backref=db.backref('PERMs', order_by=submissionTime))
  sectionID = db.Column(db.Integer, ForeignKey(Section.sectionID), primary_key=True, autoincrement=False)
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
    return "<PERM(section='%s', student='%s', blurb='%s', status='%s', submissionTime='%s', expirationTime='%s', sectionRank='%s')>" % (
      self.sectionID, self.studentID, self.blurb, self.status, self.submissionTime, self.expirationTime, self.sectionRank)

class Professor(db.Model):
  #reference teach via 'teaches'
  profID = db.Column(db.Integer, primary_key=True, autoincrement=False)
  pFirstName = db.Column(db.String(50))
  pLastName = db.Column(db.String(50))

  def __init__(self, profID, pFirstName, pLastName):
    self.profID = profID
    self.pFirstName = pFirstName
    self.pLastName = pLastName

  def __repr__(self):
    return "<Professor(profID='%s', FirstName='%s', LastName='%s')>" % (self.profID, self.pFirstName, self.pLastName)

class Teach(db.Model):
  profID = db.Column(db.Integer, ForeignKey(Professor.profID), primary_key=True, autoincrement=False)
  sectionID = db.Column(db.Integer, ForeignKey(Section.sectionID), primary_key=True,autoincrement=False)
  #reference section via 'section'
  section = db.relationship("Section", backref=db.backref('taught_by', order_by=profID))
  #reference prof via 'prof'
  prof = db.relationship("Professor", backref=db.backref('teaches', order_by=sectionID))

  def __init__(self, profID, sectionID):
    self.profID = profID
    self.sectionID = sectionID

  def __repr__(self):
    return "<Teach(profID='%s', sectionID='%s')>" % (self.profID, self.sectionID)




