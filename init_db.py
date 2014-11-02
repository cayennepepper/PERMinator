#sets up the inital database
from server import db
from server import Student

#start anew
db.drop_all()
#create all tables outlined in server.py
db.create_all()
#populate with data
db.session.add_all([(
	Student(id=45, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu"))])
db.session.commit()
