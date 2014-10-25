from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
	search_term = request.form['term']
	location = request.form['location']
	numbers = [0,1,2,3,4,5]
	links = ["http://www.facebook.com","http://www.google.com","http://www.purple.com"]
	return render_template('results.html',
		search_term = search_term,
		location = location, numbers = numbers,
		links = links)

if __name__ == '__main__':
	app.run(debug=True)