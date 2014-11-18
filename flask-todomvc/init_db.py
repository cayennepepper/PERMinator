#sets up the inital database
from server import db
from models import *
from datetime import datetime, time, timedelta

#start anew
db.drop_all()
#create all tables outlined in server.py
db.create_all()
#populate with data

db.session.add_all([(
	Student(id=45, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu")),
	(Course(id="CS133", credits=1.0)) 
	])
db.session.commit()
db.session.add_all([
	(Section(sectionNum=1, id=1, cap =20, exp = time(2), course="CS133"))
	])
db.session.commit()
db.session.add_all([
	(PERM(section = 1, student = 45, blurb = "Sarah's PERM for CS133 Section 1", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None))
	])
db.session.commit()
