from flask import Flask
app = Flask(__name__)

@app.route('/')
def index_page():
    return 'Index!'

@app.route('/perms')
def  perm_page():
	return 'PERM'

if __name__ == '__main__':
    app.run()