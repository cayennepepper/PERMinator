#sets up the inital database
from models import *
from datetime import datetime, time, timedelta

#start anew
db.drop_all()
#create all tables outlined in models.py
db.create_all()
#populate with data

db.session.add_all([(
	Student(id=45, sFirstName='Sarah', sLastName='Jundt', year=2015, college = "Pomona", sEmail = "sarah@pomona.edu", courseHistory = "Sarah's course history")),
	(Student(id=10234873, sFirstName='George', sLastName='Price', year=2015, college = "Pomona", sEmail = "gwp02011@pomona.edu", courseHistory = "ARHI         Art HistoryCOURSE_DIVBIOL         BiologyCOURSE_DIVCOMPA        Computer Science ACOURSE_DIVENGLA        English Language & CompositionCOURSE_DIVENGLI        English Literature & CompositionCOURSE_DIVHISTA        American HistoryCOURSE_DIVHISTE        European HistoryCOURSE_DIVMATHA        Mathematics Calculus ABCOURSE_DIVMATHB        Mathematics Calculus BCCOURSE_DIVPHYSB        Physics BCOURSE_DIVCOURSE_DIVBIOL040  PO  Introductory Genetics w/LabCOURSE_DIVCHEM051  PO  Gen Chemistry w/Lab AcceleratedCOURSE_DIVCHEM051 LPO  Lab, General Chemistry (Accel)COURSE_DIVHIST040  AF  History of Africa to 1800COURSE_DIVID  001  PO  Critical Inquiry Seminar: From Information to KnowledgeCOURSE_DIVPE  023  PO  Yoga - KundaliniCOURSE_DIVCOURSE_DIVBIOL041C PO  Intro Cell Chem & Cell Bio w/LabCOURSE_DIVBIOL041CLPO  Lab, Intro Cell Chem & Cell BiolCOURSE_DIVCSCI052  PO  Fundamentals of Computer ScienceCOURSE_DIVLGCS010  PO  Introduction to LinguisticsCOURSE_DIVMATH060  PO  Linear AlgebraCOURSE_DIVPE  016  PO  Weight TrainingCOURSE_DIVCOURSE_DIVCSCI062 LPO  Data Structures/Adv Program LabCOURSE_DIVCSCI081  PO  Computability & LogicCOURSE_DIVFREN044  PO  Advanced FrenchCOURSE_DIVMATH113  PO  Number Theory and CryptographyCOURSE_DIVART 027  PO  Wood SculptureCOURSE_DIVMATH103  PO  Combinatorial MathematicsCOURSE_DIVCOURSE_DIVFREN105  PO  Culture, Phonetics, and StyleCOURSE_DIVGERM001  PO  Elementary GermanCOURSE_DIVRLST158  PO  Jewish MysticismCOURSE_DIVCSCI105  HM  Computer SystemsCOURSE_DIVCSCI140  PO  AlgorithmsCOURSE_DIVCOURSE_DIVPARI001  AB  InternshipCOURSE_DIVPARI002  AB  French Language & Culture ICOURSE_DIVPARI003  AB  Literary History of 18-20CCOURSE_DIVPARI004  AB  French Lexical Units-SentenceCOURSE_DIVPARI005  AB  The European UnionCOURSE_DIVCOURSE_DIVCSCI133  PO  Database SystemsCOURSE_DIVCSCI159  PO  Natural Language Processing                 COURSE_DIVCSCI190  PO  Computer Science Senior Seminar                                                        COURSE_DIVFREN015  PO  Advanced Plus ConversationCOURSE_DIVRUSS001  PO  Elementary RussianCOURSE_DIVCOURSE_DIVCSCI131  HM  Programming Languages COURSE_DIVCSCI151  HM  Artificial Intelligence COURSE_DIVCSCI181B HM  Advanced Topics in Algorithms / Computer Science Seminar  COURSE_DIVCSCI192  PO  Senior Project  COURSE_DIVRLST142  AF  Prob of Evil: Afr-Amer Engagmnts")),
	(Student(id=123, sFirstName='Anna', sLastName='Turner', year=2015, college="Pomona", sEmail="anna@edu", courseHistory = "Anna's course history")),
	(Course(id="CS133", credits=1.0)),
	(Course(id="RLST40", credits=1.0)),
	(Professor(profID=90, pFirstName="Melanie", pLastName="Wu")),
	])
db.session.commit()
db.session.add_all([
	(Section( id=1,sectionNum=1, cap =20, exp = timedelta(days=14), course="CS133")),
	(Section( id=2,sectionNum=1, cap =40, exp = timedelta(days=14), course="RLST40")),
	])
db.session.commit()
print "Okay"
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

