#database schema: sets up the inital database
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0")

Base = declarative_base()

#students table
class Student(Base):
     __tablename__ = 'students'

     id = Column(Integer, primary_key=True)
     sFirstName = Column(String(50))
     sLastName = Column(String(50))
     year = Column(Integer)
     college = Column(String(6))
     sEmail = Column(String(50))

     def __repr__(self):
        return "<Student(sFirstName='%s', sLastName='%s', year='%s', college='%s', sEmail='%s')>" % (
                             self.sFirstName, self.sLastName, self.year, self.college,self.sEmail)

Base.metadata.create_all(engine)