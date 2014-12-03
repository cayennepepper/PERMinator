#sets up the inital database
from models import *
from datetime import datetime, time, timedelta

#start anew
db.drop_all()
#create all tables outlined in server.py
db.create_all()
#populate with data

db.session.add_all([(
	Student(id=45, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu")),
	(Student(id=10234873, sFirstName='George', sLastName='Price', year=2015, college = "Pomona", sEmail = "gwp02011@pomona.edu")),
	(Student(id=123, sFirstName='Anna', sLastName='Turner', year=2015, college="Pomona", sEmail="anna@edu")),
	(Course(id="CS133", credits=1.0)),
	(Course(id="RLST40", credits=1.0)),
	(Professor(profID=90, pFirstName="Melanie", pLastName="Wu")),
	])
db.session.commit()
db.session.add_all([
	(Section( id=1,sectionNum=1, cap =20, exp = timedelta(days=14), course="CS133")),
	(Section( id=3,sectionNum=2, cap =20, exp = timedelta(days=14), course="CS133")),
	(Section( id=2,sectionNum=1, cap =40, exp = timedelta(days=14), course="RLST40")),
	])
db.session.commit()
print "Okay"
db.session.add_all([
	(PERM(section = 1, student = 45, blurb = "Sarah's PERM for CS133 Section 1", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 1)),
	(PERM(section = 3, student =45 , blurb = "Sarah's PERM for CS133 Section 2", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 2)),
	(PERM(section = 1, student = 10234873, blurb = "Potential CS minor with a lot of interests", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None))
	])
db.session.add_all([
	(Teach(profID=90, sectionID=1)),
	(Teach(profID=90, sectionID=3)),
	(Major(college="Pomona", name="Computer Science")),
	(Major(college="HMC", name="Computer Science")),
	(Major(college="Pitzer", name="French")),
	(Major(college="Pomona", name="Biology"))
	])
db.session.commit()
pomona_cs_major = db.session.query(Major).filter(Major.college=="Pomona" and Major.name=="Computer Science").first()
pomona_bio_major = db.session.query(Major).filter(Major.college=="HMC" and Major.name=="Computer Science").first()
pitzer_fr_major = db.session.query(Major).filter(Major.college=="Pitzer" and Major.name=="French").first()
db.session.add_all([
	(MajorsIn(majorID=pitzer_fr_major.id, studentID=10234873)),
	(MajorsIn(majorID=pomona_cs_major.id, studentID=10234873)),
	(MajorsIn(majorID=pomona_bio_major.id, studentID=45)),
	(MajorsIn(majorID=pomona_cs_major.id, studentID=45))
	])
db.session.commit()

