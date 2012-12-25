import sqlite3
from flask import Flask, render_template, g, url_for, json, Response, request
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
		methods = [m for m in rule.methods if m != 'HEAD' and m != 'OPTIONS']
		routes.append('%-6s'%list(methods)[0] + ' ' + str(rule))
	routes.sort(cmp=lambda a,b: cmp(a.split()[1], b.split()[1]))
	return Response('sitemap:'+json.dumps(routes, indent=2), mimetype='text/plain')


#
# Companies API
#
@app.route('/companies')
def companies():
	companies = query_db('select * from companies')
	return json.dumps(companies)

@app.route('/companies', methods=['POST'])
def post_company():
	g.db.execute('insert into companies (name) values (?)', (request.json['name'],))
	company_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return json.dumps(company_id)

@app.route('/companies/<company_id>')
def company(company_id):
	companies = query_db('select * from companies where id=?', company_id)
	return json.dumps(companies[0])

@app.route('/companies/<company_id>', methods=['PUT'])
def put_company(company_id):
	g.db.execute('update companies set name=? where id=?', (request.json['name'], company_id))
	g.db.commit()
	companies = query_db('select * from companies where id=?', company_id)
	return json.dumps(companies[0])

@app.route('/companies/<company_id>', methods=['DELETE'])
def delete_company(company_id):
	g.db.execute('delete from companies where id=?', (company_id,))
	g.db.commit()
	return 'success'

@app.route('/companies/<company_id>/projects')
def company_projects(company_id):
	projects = query_db('select * from projects where company_id=?', company_id)
	return json.dumps(projects)


#
# Projects API
#
@app.route('/projects')
def projects():
	projects = query_db('select * from projects')
	return json.dumps(projects)

@app.route('/projects', methods=['POST'])
def post_project():
	g.db.execute('insert into projects (name, company_id) values (?, ?)', (request.json['name'],request.json['company_id']))
	project_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return json.dumps(project_id)

@app.route('/projects/<project_id>')
def project(project_id):
	projects = query_db('select * from projects where id = ?', project_id)
	return json.dumps(projects[0])

@app.route('/projects/<project_id>', methods=['PUT'])
def put_project(project_id):
	g.db.execute('update projects set name=? where id=?', (request.json['name'], project_id))
	g.db.commit()
	projects = query_db('select * from projects where id=?', project_id)
	return json.dumps(projects[0])

@app.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
	g.db.execute('delete from projects where id=?', (project_id,))
	g.db.commit()
	return 'success'

@app.route('/projects/<project_id>/tasks')
def project_tasks(project_id):
	tasks = query_db('select * from tasks where project_id = ?', project_id)
	return json.dumps(tasks)


#
# Tasks API
#
@app.route('/tasks')
def tasks():
	tasks = query_db('select * from tasks')
	return json.dumps(tasks)

@app.route('/tasks', methods=['POST'])
def post_task():
	g.db.execute('insert into tasks (title, project_id, date_created) values (?, ?, current_timestamp)', (request.json['title'],request.json['project_id']))
	task_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return json.dumps(task_id)

@app.route('/tasks/<task_id>')
def task(task_id):
	tasks = query_db('select * from tasks where id=?', task_id)
	return json.dumps(tasks[0])

@app.route('/tasks/<task_id>', methods=['PUT'])
def put_task(task_id):
	g.db.execute('update tasks set title=?, project_id=? where id=?', (request.json['title'], request.json['project_id'], task_id))
	g.db.commit()
	tasks = query_db('select * from tasks where id=?', task_id)
	return json.dumps(tasks[0])

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
	g.db.execute('delete from tasks where id=?', (task_id,))
	g.db.commit()
	return 'success'

@app.route('/tasks/<task_id>/notes')
def task_notes(task_id):
	notes = query_db('select * from notes where task_id=?', task_id)
	return json.dumps(notes)


#
# Notes API
#
@app.route('/notes')
def notes():
	notes = query_db('select * from notes')
	return json.dumps(notes)

@app.route('/notes', methods=['POST'])
def post_note():
	g.db.execute('insert into notes (text, task_id) values (?, ?)', (request.json['text'],request.json['task_id']))
	task_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return json.dumps(task_id)

@app.route('/notes/<note_id>')
def note(note_id):
	notes = query_db('select * from notes where id=?', note_id)
	return json.dumps(notes[0])

@app.route('/notes/<note_id>', methods=['PUT'])
def put_note(note_id):
	g.db.execute('update notes set text=? where id=?', (request.json['text'], note_id))
	g.db.commit()
	notes = query_db('select * from notes where id=?', note_id)
	return json.dumps(notes[0])

@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
	g.db.execute('delete from notes where id=?', (note_id,))
	g.db.commit()
	return 'success'


#
# Users API
#
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


