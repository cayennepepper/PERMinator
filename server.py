from flask import Flask
from flask import render_template
from flask.ext.sqlalchemy import SQLAlchemy

from flask.ext.triangle import Triangle

app = Flask(__name__, template_folder="app", static_path='/static')
Triangle(app)
#sets up db connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0'
db = SQLAlchemy(app)

#DB SCHEMA: STUDENT MODEL
class Student(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=False)
  sFirstName = db.Column(db.String(50))
  sLastName = db.Column(db.String(50))
  year = db.Column(db.Integer)
  college = db.Column(db.String(6))
  sEmail = db.Column(db.String(50))

  def __init__(self, id, sFirstName, sLastName, year, college, sEmail):
    self.id = id
    self.sFirstName = sFirstName
    self.sLastName = sLastName
    self.year = year
    self.college = college
    self.sEmail = sEmail
    
  def __repr__(self):
    return "<Student(id='%s', sFirstName='%s', sLastName='%s', year='%s', college='%s', sEmail='%s')>" % (
      self.id, self.sFirstName, self.sLastName, self.year, self.college,self.sEmail)

@app.route('/')
def index_page():
	return render_template('view1/view1.html')

@app.route('/professor/<pid>')
def  professor_home(pid): 
	return 'HOME PAGE FOR PROFESSOR '+pid

@app.route('/student/<sid>')
def  student_home(sid):
	return render_template('student/studentHome.html')

@app.route('/myCourse/<cid>')
def  course(cid):
	return 'COURSE '+cid

@app.route('/deptCourse/<cid>')
def  dept_course(cid):
	return 'DEPT COURSE '+cid

@app.route('/student/<sid>/edit')
def  edit_perms(sid):
	return 'EDIT PERMS '

@app.route('/student/<sid>/submit')
def  submit_perms(sid):
	return 'SUBMIT PERMS '

if __name__ == '__main__':
    app.run(debug=True)