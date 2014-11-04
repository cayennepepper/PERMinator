from flask import Flask, render_template
from flask.ext.triangle import Triangle


app = Flask(__name__, template_folder="app", static_path='/static')
Triangle(app)


@app.route('/')
def index():
    return render_template('view1/view1.html')


if __name__ == '__main__':
    app.run()