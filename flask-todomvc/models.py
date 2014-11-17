from server import db
from sqlalchemy import ForeignKey

#DB SCHEMA: STUDENT MODEL
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

class Course(db.Model):
  courseID = db.Column(db.Integer, primary_key=True, autoincrement=False)
  credits = db.Column(db.Numeric)

  def __init__(self, id, credits):
    self.courseID = id
    self.credits = credits

  def __repr__(self):
    return "<Course(courseID='%s', credits='%s')>" % (self.courseID, self.credits)

class Section(db.Model):
  sectionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
  enrollmentCap = db.Column(db.Integer)
  defaultExpiration = db.Column(db.Time)
  courseID = db.Column(db.Integer, ForeignKey(Course.courseID))

  def __init__(self,id,cap,exp,course):
    self.sectionID = id
    self.enrollmentCap = cap
    self.defaultExpiration = exp
    self.courseID = course

  def __repr__(self):
    return "<Section(sectionID='%s', enrollmentCap='%s', defaultExpiration='%s', courseID='%s')>" % (
      self.sectionID, self.enrollmentCap, self.defaultExpiration, self.courseID)

class PERM(db.Model):
  section = db.Column(db.Integer, ForeignKey(Section.sectionID), primary_key=True, autoincrement=False)
  student = db.Column(db.Integer, ForeignKey(Student.id), primary_key=True, autoincrement=False)
  blurb = db.Column(db.String(200))
  status = db.Column(db.Enum("Revoked", "Approved", "Denied", "Cancelled"))
  submissionTime = db.Column(db.DateTime)
  expirationTime = db.Column(db.DateTime)
  sectionRank = db.Column(db.Integer)

  def __init__(self,section,student,blurb,status,submissionTime,expirationTime,sectionRank):
    self.section = section
    self.student = student
    self.blurb = blurb
    self.status = status
    self.submissionTime = submissionTime
    self.expirationTime = expirationTime
    self.sectionRank = sectionRank

  def __repr__(self):
    return "<PERM(section='%s', student='%s', blurb='%s', status='%s', submissionTime='%s', expirationTime='%s', sectionRank='%s')>" % (
      self.section, self.student, self.blurb, self.status, self.submissionTime, self.expirationTime, self.sectionRank)

class Professor(db.Model):
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
  prof = db.Column(db.Integer, ForeignKey(Professor.profID), primary_key=True, autoincrement=False)
  section = db.Column(db.Integer, ForeignKey(Section.sectionID), primary_key=True,autoincrement=False)



