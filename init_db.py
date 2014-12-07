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
	(Student(id=10234873, sFirstName='George', sLastName='Price', year=2015, college = "Pomona", sEmail = "gwp02011@pomona.edu", courseHistory = "ARHI         Art HistoryCOURSE_DIVBIOL         BiologyCOURSE_DIVCOMPA        Computer Science ACOURSE_DIVENGLA        English Language & CompositionCOURSE_DIVENGLI        English Literature & CompositionCOURSE_DIVHISTA        American HistoryCOURSE_DIVHISTE        European HistoryCOURSE_DIVMATHA        Mathematics Calculus ABCOURSE_DIVMATHB        Mathematics Calculus BCCOURSE_DIVPHYSB        Physics BCOURSE_DIVBIOL040  PO  Introductory Genetics w/LabCOURSE_DIVCHEM051  PO  Gen Chemistry w/Lab AcceleratedCOURSE_DIVCHEM051 LPO  Lab, General Chemistry (Accel)COURSE_DIVHIST040  AF  History of Africa to 1800COURSE_DIVID  001  PO  Critical Inquiry Seminar: From Information to KnowledgeCOURSE_DIVPE  023  PO  Yoga - KundaliniCOURSE_DIVBIOL041C PO  Intro Cell Chem & Cell Bio w/LabCOURSE_DIVBIOL041CLPO  Lab, Intro Cell Chem & Cell BiolCOURSE_DIVCSCI052  PO  Fundamentals of Computer ScienceCOURSE_DIVLGCS010  PO  Introduction to LinguisticsCOURSE_DIVMATH060  PO  Linear AlgebraCOURSE_DIVPE  016  PO  Weight TrainingCOURSE_DIVCSCI062 LPO  Data Structures/Adv Program LabCOURSE_DIVCSCI081  PO  Computability & LogicCOURSE_DIVFREN044  PO  Advanced FrenchCOURSE_DIVMATH113  PO  Number Theory and CryptographyCOURSE_DIVART 027  PO  Wood SculptureCOURSE_DIVMATH103  PO  Combinatorial MathematicsCOURSE_DIVFREN105  PO  Culture, Phonetics, and StyleCOURSE_DIVGERM001  PO  Elementary GermanCOURSE_DIVRLST158  PO  Jewish MysticismCOURSE_DIVCSCI105  HM  Computer SystemsCOURSE_DIVCSCI140  PO  AlgorithmsCOURSE_DIVPARI001  AB  InternshipCOURSE_DIVPARI002  AB  French Language & Culture ICOURSE_DIVPARI003  AB  Literary History of 18-20CCOURSE_DIVPARI004  AB  French Lexical Units-SentenceCOURSE_DIVPARI005  AB  The European UnionCOURSE_DIVCSCI133  PO  Database SystemsCOURSE_DIVCSCI159  PO  Natural Language Processing                 COURSE_DIVCSCI190  PO  Computer Science Senior Seminar                                                        COURSE_DIVFREN015  PO  Advanced Plus ConversationCOURSE_DIVRUSS001  PO  Elementary RussianCOURSE_DIVCSCI131  HM  Programming Languages COURSE_DIVCSCI151  HM  Artificial Intelligence COURSE_DIVCSCI181B HM  Advanced Topics in Algorithms / Computer Science Seminar  COURSE_DIVCSCI192  PO  Senior Project  COURSE_DIVRLST142  AF  Prob of Evil: Afr-Amer Engagmnts")),
	(Student(id=123, sFirstName='Anna', sLastName='Turner', year=2015, college="Pomona", sEmail="anna@edu", courseHistory = "Anna's course history")),
	(Course(id="CS133")),
	(Course(id="RLST40")),
	(Professor(profID=90, pFirstName="Melanie", pLastName="Wu")),
	])
db.session.commit()
db.session.add_all([
	(Section( id=1,sectionNum=1, course="CS133")),
	(Section( id=3,sectionNum=2, course="CS133")),
	(Section( id=4,sectionNum=3, course="CS133")),
	(Section( id=2,sectionNum=1, course="RLST40")),
	])
db.session.commit()
print "Okay"
db.session.add_all([
	(PERM(section = 1, student = 45, blurb = "Sarah's PERM for CS133 Section 1", 
		status = "Expired", submissionTime = datetime.now(), expirationTime = (datetime.now()-timedelta(days=10)), sectionRank = 1)),
	(PERM(section = 4, student =45 , blurb = "Sarah's PERM for CS133 Section 3", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = 2)),
	(PERM(section = 1, student = 10234873, blurb = "Potential CS minor with a lot of interests", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None)),
	(PERM(section = 1, student = 123, blurb = "Blurbey", 
		status = "Requested", submissionTime = datetime.now(), expirationTime = (datetime.now()+timedelta(days=10)), sectionRank = None))
	])
db.session.add_all([
	(Teach(profID=90, sectionID=1)),
	(Teach(profID=90, sectionID=3)),
	(Teach(profID=90, sectionID=4)),
	(Major(college="Pomona", name="Computer Science", satisfiedBy="CSCI 051	CSCI 051G	CSCI 052	CSCI 055	CSCI 062	CSCI 081	CSCI 105	CSCI 131	CSCI 140	CSCI 151	CSCI 158	CSCI 159	CSCI 181H 	CSCI 181J 	CSCI 181K 	CSCI 190	CSCI 191	CSCI 192	CSCI 199DRPO 	CSCI 199IRPO 	CSCI 199RAPO	CSCI 133	CSCI 135	CSCI 124	CSCI 125	CSCI 132	CSCI 134	CSCI 136	CSCI 141	CSCI 142	CSCI 144	CSCI 147	CSCI 152	CSCI 153	CSCI 154	CSCI 155	CSCI 156	CSCI 157	CSCI 183	CSCI 184	MATH 031	MATH 060	MATH 055	MATH 103")),
	(Major(college="HMC", name="Computer Science", satisfiedBy="CSCI 005	CSCI 060	CSCI 070	CSCI 055	CSCI 062	CSCI 081	CSCI 105	CSCI 131	CSCI 140	CSCI 151	CSCI 158	CSCI 159	CSCI 181H 	CSCI 181J 	CSCI 181K 	CSCI 190	CSCI 191	CSCI 192	CSCI 199DRPO 	CSCI 199IRPO 	CSCI 199RAPO	CSCI 133	CSCI 135	CSCI 124	CSCI 125	CSCI 132	CSCI 134	CSCI 136	CSCI 141	CSCI 142	CSCI 144	CSCI 147	CSCI 152	CSCI 153	CSCI 154	CSCI 155	CSCI 156	CSCI 157	CSCI 183	CSCI 184	MATH 031	MATH 060	MATH 055	MATH 103")),
	(Major(college="Pitzer", name="French", satisfiedBy="French courses")),
	(Major(college="Pomona", name="Biology", satisfiedBy="Biology courses")),
	(Major(college="CMC", name="Religious Studies", satisfiedBy="Religious studies courses")),
	])
db.session.commit()
pomona_cs_major = db.session.query(Major).filter(Major.college=="Pomona" and Major.name=="Computer Science").first()
pomona_bio_major = db.session.query(Major).filter(Major.college=="HMC" and Major.name=="Computer Science").first()
pitzer_fr_major = db.session.query(Major).filter(Major.college=="Pitzer" and Major.name=="French").first()
cmc_rs_major = db.session.query(Major).filter(Major.college=="CMC" and Major.name=="Religious Studies").first()
db.session.add_all([
	(MajorsIn(majorID=pitzer_fr_major.id, studentID=10234873)),
	(MajorsIn(majorID=pomona_bio_major.id, studentID=45)),
	(MajorsIn(majorID=pomona_cs_major.id, studentID=45)),
	(MajorsIn(majorID=cmc_rs_major.id, studentID=123)),
	(SatisfiesMajor(majorID=pomona_cs_major.id, courseID="CS133")),
	(SatisfiesMajor(majorID=cmc_rs_major.id, courseID="RLST40")),
	])
db.session.commit()

