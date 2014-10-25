from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index_page():
	return render_template('index.html')

@app.route('/professor/<pid>')
def  professor_home(pid): 
	return 'HOME PAGE FOR PROFESSOR '+pid

@app.route('/student/<sid>')
def  student_home(sid):
	return 'PERMS FOR '+sid

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