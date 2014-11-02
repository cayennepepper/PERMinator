#database schema: sets up the inital database
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0")
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

#DECLARE SCHEMA
#students table
class Student(Base):
     __tablename__ = 'students'

     id = Column(Integer, primary_key=True, autoincrement=False)
     sFirstName = Column(String(50))
     sLastName = Column(String(50))
     year = Column(Integer)
     college = Column(String(6))
     sEmail = Column(String(50))

     def __repr__(self):
        return "<Student(id='%s', sFirstName='%s', sLastName='%s', year='%s', college='%s', sEmail='%s')>" % (
                             self.id, self.sFirstName, self.sLastName, self.year, self.college,self.sEmail)

Base.metadata.create_all(engine)

#POPULATE WITH INITIAL DATA
#students table
session.query(Student).delete()
session.add_all([(
	Student(id=90, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu"))])
session.commit()
session.close()