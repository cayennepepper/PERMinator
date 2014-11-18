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
	(Teach(profID=90, sectionID=1))
	])
db.session.commit()
