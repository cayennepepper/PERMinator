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
	(Course(id="CS133", credits=1.0)),
	(Professor(profID=90, pFirstName="Melanie", pLastName="Wu")),
	])
db.session.commit()
db.session.add_all([
	(Section( id=1,sectionNum=1, cap =20, exp = timedelta(days=14), course="CS133"))
	])
db.session.commit()
db.session.add_all([
	(PERM(section = 1, student = 45, blurb = "Sarah's PERM for CS133 Section 1", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None)),
	(PERM(section = 1, student = 10234873, blurb = "Potential CS minor with a lot of interests", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None))
	])
db.session.add_all([
	(Teach(profID=90, sectionID=1)),
	(Major(college="Pomona", name="Computer Science")),
	(Major(college="HMC", name="Computer Science")),
	(Major(college="Pomona", name="Biology"))
	])
db.session.commit()
pomona_cs_major = db.session.query(Major).filter(Major.college=="Pomona" and Major.name=="Computer Science").first()
db.session.add_all([
	(MajorsIn(majorID=pomona_cs_major.id, studentID=45)),
	(MajorsIn(majorID=pomona_cs_major.id, studentID=10234873))
	])
db.session.commit()
