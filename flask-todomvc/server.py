""" server.py """
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request)
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path='')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost/PERMinator?charset=utf8&use_unicode=0'
db = SQLAlchemy(app)

class Item(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))

  def __init__(self, json):
    print json
    self.title = json[u'title']

  def __repr__(self):
    return "<Item(id='%s', title='%s')>" % (self.id, self.title)

  def serialize(self): #lets us serialize it!!
        result = {}
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self,key)
        return result

db.create_all();

@app.route('/student/<student:id>')
def index():
    todos = db.session.query(Item).all()
    _todos = [todo.serialize() for todo in todos if todo!=None]
    return render_template('index.html', todos=_todos)

@app.route('/')
def index():
    todos = db.session.query(Item).all()
    _todos = [todo.serialize() for todo in todos if todo!=None]
    return render_template('index.html', todos=_todos)


@app.route('/todos/', methods=['POST'])
def todo_create():
    todo = request.get_json()
    db.session.add(Item(todo))
    db.session.commit()
    return "Good"


@app.route('/todos/<int:id>')
def todo_read(id):
    todo = db.session.query(Item).filter(Item.id==id).first()
    if todo==None:
        abort(404) #send error message
    return jsonify(todo.serialize())


@app.route('/todos/<int:id>', methods=['PUT', 'PATCH'])
def todo_update(id):
    new_item = request.get_json()
    print request.get_json
    print new_item[u'title']
    db.session.query(Item).filter(Item.id==id).update({Item.title:new_item[u'title']})
    print "NEW IN DB:", db.session.query(Item).filter(Item.id==id).all()
    db.session.commit()
    return "Fine"


@app.route('/todos/<int:id>', methods=['DELETE'])
def todo_delete(id):
    db.session.query(Item).filter(Item.id==id).delete()
    db.session.commit()
    return "Fine"

if __name__ == '__main__':
    app.run(port=8000)
