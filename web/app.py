import sqlite3

from flask import Flask, g, render_template, request, url_for

DATABASE = '../test.sqlite'

app = Flask(__name__)

def get_db():
	db = getattr(g, '_database', None)
	if db is None:
		db = g._databse = sqlite3.connect(DATABASE)
	return db

@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()

@app.route('/<name>')
def hello(name=None):
	get_db()
	return render_template('hello.html', name=name)

# with app.test_request_context():
#     print(url_for('biblethumb'))
#     print(url_for('biblethumb', next='008'))
#     print(url_for('biblethumb', usernam='Mother Fucker'))
