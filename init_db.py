#sets up the inital database
from models import *
from datetime import datetime, time, timedelta

#start anew
db.drop_all()
#create all tables outlined in models.py
db.create_all()
#populate with data

db.session.add_all([(
	Student(id=45, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu")),
	(Student(id=10234873, sFirstName='George', sLastName='Price', year=2015, college = "Pomona", sEmail = "gwp02011@pomona.edu")),
	(Student(id=123, sFirstName='Anna', sLastName='Turner', year=2015, college="Pomona", sEmail="anna@edu")),
	(Student(id=007, sFirstName='Mauricio', sLastName='Molina', year=2015, college="Pomona", sEmail="mauricio@edu")),
	(Course(id="CSCI133")),
	(Course(id="RLST40")),
	(Course(id="CSCI55")),
	(Course(id="CSCI52")),
	(Course(id="CSCI62")),
	(Course(id="CSCI51")),
	(Course(id="MATH121")),
	(Course(id="ANTH10")),
	(Course(id="BIOL41C")),
	(Course(id="BIOL40")),
	(Course(id="NEUR101")),
	(Course(id="FREN33")),

	(Professor(profID=90, pFirstName="Melanie", pLastName="Wu"))
	])
db.session.commit()
db.session.add_all([
	(Section( id=1,sectionNum=1, course="CSCI133")),
	(Section( id=3,sectionNum=2, course="CSCI133")),
	(Section( id=4,sectionNum=3, course="CSCI133")),
	(Section( id=2,sectionNum=1, course="RLST40")),
	(Section( id=5,sectionNum=1, course="CSCI51")),
	(Section( id=10,sectionNum=1, course="BIOL40")),
	(HasTaken(courseID="CSCI133", studentID=45)),
	(HasTaken(courseID="CSCI133", studentID=123)),
	(HasTaken(courseID="CSCI133", studentID=10234873)),
	(HasTaken(courseID="RLST40", studentID=10234873)),
	(HasTaken(courseID="RLST40", studentID=007)),
	(HasTaken(courseID="CSCI55", studentID=007)),
	(HasTaken(courseID="CSCI62", studentID=007)),
	(HasTaken(courseID="CSCI51", studentID=007)),
	(HasTaken(courseID="MATH121", studentID=007)),
	(HasTaken(courseID="BIOL41C", studentID=007)),
	(HasTaken(courseID="BIOL40", studentID=007)),
	(HasTaken(courseID="NEUR101", studentID=007)),
	(HasTaken(courseID="FREN33", studentID=007)),
	(HasTaken(courseID="FREN33", studentID=10234873))
	])
db.session.commit()
print "Okay"
db.session.add_all([
	(PERM(section = 1, student = 45, blurb = "Sarah's PERM for CSCI133 Section 1", 
		status = "Expired", submissionTime = datetime.now(), expirationTime = (datetime.now()-timedelta(days=1)), sectionRank = 1)),
	(PERM(section = 4, student =45 , blurb = "Sarah's PERM for CSCI133 Section 3", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 2)),
	(PERM(section = 1, student = 10234873, blurb = "Potential CS minor with a lot of interests",
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None)),
	(PERM(section = 10, student = 7, blurb = "Please let me take this class!!", 
		status = "Approved", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 1)),
	(PERM(section = 2, student = 7, blurb = "I'll get into this class", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 1)),
	(PERM(section = 3, student = 7, blurb = "I love databases!!", 
		status = "Expired", submissionTime = datetime.now(), expirationTime = (datetime.now()-timedelta(days=10)), sectionRank = 1)),
	(PERM(section = 1, student = 123, blurb = "Blurbey", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 1))
	])
db.session.add_all([
	(Teach(profID=90, sectionID=1)),
	(Teach(profID=90, sectionID=3)),
	(Teach(profID=90, sectionID=4)),
	(Teach(profID=90, sectionID=5)),
	(Major(college="Pomona", name="Computer Science")),
	(Major(college="HMC", name="Computer Science")),
	(Major(college="Pitzer", name="French")),
	(Major(college="Pomona", name="Biology")),
	(Major(college="CMC", name="Religious Studies")),
	])
db.session.commit()
pomona_cs_major = db.session.query(Major).filter(Major.college=="Pomona" and Major.name=="Computer Science").first()
pomona_bio_major = db.session.query(Major).filter(Major.college=="Pomona" and Major.name=="Biology").first()
pitzer_fr_major = db.session.query(Major).filter(Major.college=="Pitzer" and Major.name=="French").first()
cmc_rs_major = db.session.query(Major).filter(Major.college=="CMC" and Major.name=="Religious Studies").first()
db.session.add_all([
	(MajorsIn(majorID=pitzer_fr_major.id, studentID=10234873)),
	(MajorsIn(majorID=pomona_bio_major.id, studentID=007)),
	(MajorsIn(majorID=pomona_cs_major.id, studentID=45)),
	(MajorsIn(majorID=cmc_rs_major.id, studentID=123)),
	(SatisfiesMajor(majorID=pomona_cs_major.id, courseID="CSCI133")),
	(SatisfiesMajor(majorID=cmc_rs_major.id, courseID="RLST40")),
	])
db.session.commit()
