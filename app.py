import sqlite3
from flask import Flask, render_template, g
import json
app = Flask(__name__)

DATABASE = 'test.db'

def query_db(query):
	r = g.db.execute(query)
	cols = [d[0] for d in r.description]
	result = [dict(zip(cols, row)) for row in r.fetchall()]
	return result

@app.before_request
def before_request():
	g.db = sqlite3.connect(DATABASE)

@app.teardown_request
def teardown_request(exception):
	if hasattr(g, 'db'):
		g.db.close()



@app.route('/')
def index():
	users = query_db('select * from users')
	return json.dumps(users)

if __name__ == '__main__':
	app.run(debug=True)
