import sqlite3
from flask import Flask, render_template, g, url_for, json, Response
app = Flask(__name__)

DATABASE = 'test.db'

def query_db(query, *args):
	r = g.db.execute(query, args)
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

@app.route("/sitemap")
def sitemap():
	routes = []
	for rule in app.url_map.iter_rules():
		if "GET" in rule.methods:
			routes.append(str(rule))
	routes.sort()
	return Response(json.dumps(routes), mimetype='application/json')


@app.route('/companies')
def companies():
	companies = query_db('select * from companies')
	return json.dumps(companies)

@app.route('/companies/<company_id>')
def company(company_id):
	companies = query_db('select * from companies where id=?', company_id)
	return json.dumps(companies[0])

@app.route('/companies/<company_id>/projects')
def company_projects(company_id):
	projects = query_db('select * from projects where company_id=?', company_id)
	return json.dumps(projects)

@app.route('/projects')
def projects():
	projects = query_db('select * from projects')
	return json.dumps(projects)

@app.route('/projects/<project_id>')
def project(project_id):
	projects = query_db('select * from projects where id = ?', project_id)
	return json.dumps(projects[0])

@app.route('/projects/<project_id>/tasks')
def project_tasks(project_id):
	tasks = query_db('select * from tasks where project_id = ?', project_id)
	return json.dumps(tasks)

@app.route('/tasks')
def tasks():
	tasks = query_db('select * from tasks')
	return json.dumps(tasks)

@app.route('/tasks/<task_id>')
def task(task_id):
	tasks = query_db('select * from tasks where id=?', task_id)
	return json.dumps(tasks[0])

@app.route('/tasks/<task_id>/notes')
def task_notes(task_id):
	notes = query_db('select * from notes where task_id=?', task_id)
	return json.dumps(notes)

@app.route('/notes')
def notes():
	notes = query_db('select * from notes')
	return json.dumps(notes)

@app.route('/notes/<note_id>')
def note(note_id):
	notes = query_db('select * from notes where id=?', note_id)
	return json.dumps(notes[0])

@app.route('/users')
def users():
	users = query_db('select * from users')
	return json.dumps(users)

@app.route('/users/<user_id>')
def user(user_id):
	users = query_db('select * from users where id=?', user_id)
	return json.dumps(users[0])

@app.route('/users/<user_id>/tasks')
def user_tasks(user_id):
	tasks = query_db('select * from tasks where owner_id=?', user_id)
	return json.dumps(tasks)



if __name__ == '__main__':
	app.run(debug=True)


