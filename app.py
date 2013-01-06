from functools import wraps
import sqlite3
import jsonschema
from flask import Flask, render_template, g, url_for, json, Response, request, abort, jsonify, session
app = Flask(__name__)

app.config['DATABASE'] = 'test.db'
app.secret_key = '\xafW>\xe9\xa1\xc0\x7f\x05\x86\xdb%g\x87\x8c_\x7fD\x0f\x81\x0cS.\xca\xbf'
current_user = None


def require_login(fn):
	@wraps(fn)
	def wrapped(*args, **kwargs):
		response = Response('Login Required', status=403)
		user_id = request.cookies.get('session', None)
		if user_id == None:
			return response
		users = query_db('select * from users where id=?', user_id)
		if len(users) == 0:
			return response
		global current_user
		current_user = users[0]
		return fn(*args, **kwargs)
	return wrapped

def json_validate(schema):
	def decorator(f):
		@wraps(f)
		def decorated_function(*args, **kwargs):
			v = jsonschema.Draft3Validator(schema)
			errors = [str(error) for error in v.iter_errors(request.json)]
			if len(errors) > 0:
				return JSONResponse({'errors':errors}, 400)
			return f(*args, **kwargs)
		return decorated_function
	return decorator


def query_db(query, *args):
	r = g.db.execute(query, args)
	cols = [d[0] for d in r.description]
	result = [dict(zip(cols, row)) for row in r.fetchall()]
	return result

@app.before_request
def before_request():
	g.db = sqlite3.connect(app.config['DATABASE'])

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
	return Response(json.dumps(routes, indent=2), mimetype='text/plain')

def JSONResponse(data, status=200):
	response = jsonify(data)
	response.status_code = status
	return response

#
# Companies API
#
@app.route('/companies')
def companies():
	companies = query_db('select * from companies')
	return JSONResponse({'items':companies})

@app.route('/companies', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'name': { 'type': 'string' }
		}
	}
)
def post_company():
	g.db.execute('insert into companies (name) values (?)', (request.json['name'],))
	company_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return JSONResponse({'result':company_id}, 201)

@app.route('/companies/<company_id>')
def company(company_id):
	companies = query_db('select * from companies where id=?', company_id)
	if len(companies) == 0:
		return abort(404)
	return JSONResponse(companies[0])

@app.route('/companies/<company_id>', methods=['PUT'])
def put_company(company_id):
	exists = g.db.execute('select exists(select * from companies where id=?)', (company_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('update companies set name=? where id=?', (request.json['name'], company_id))
	g.db.commit()
	companies = query_db('select * from companies where id=?', company_id)
	return Response('', 204)

@app.route('/companies/<company_id>', methods=['DELETE'])
def delete_company(company_id):
	exists = g.db.execute('select exists(select * from companies where id=?)', (company_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('delete from companies where id=?', (company_id,))
	g.db.commit()
	return Response('', 204)

@app.route('/companies/<company_id>/projects')
def company_projects(company_id):
	projects = query_db('select * from projects where company_id=?', company_id)
	return JSONResponse({'items':projects})


#
# Projects API
#
@app.route('/projects')
def projects():
	projects = query_db('select * from projects')
	return JSONResponse({'items':projects})

@app.route('/projects', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'name': { 'type': 'string' },
			'company_id': { 'type': 'integer' }
		}
	}
)
def post_project():
	g.db.execute('insert into projects (name, company_id) values (?, ?)', (request.json['name'],request.json['company_id']))
	project_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return JSONResponse({'result':project_id}, 201)

@app.route('/projects/<project_id>')
def project(project_id):
	projects = query_db('select * from projects where id = ?', project_id)
	if len(projects) == 0:
		return abort(404)
	return JSONResponse(projects[0])

@app.route('/projects/<project_id>', methods=['PUT'])
def put_project(project_id):
	exists = g.db.execute('select exists(select * from projects where id=?)', (project_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('update projects set name=? where id=?', (request.json['name'], project_id))
	g.db.commit()
	projects = query_db('select * from projects where id=?', project_id)
	return Response('', 204)

@app.route('/projects/<project_id>', methods=['DELETE'])
def delete_project(project_id):
	exists = g.db.execute('select exists(select * from projects where id=?)', (project_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('delete from projects where id=?', (project_id,))
	g.db.commit()
	return Response('', 204)

@app.route('/projects/<project_id>/tasks')
def project_tasks(project_id):
	tasks = query_db('select * from tasks where project_id = ?', project_id)
	return JSONResponse({'items':tasks})


#
# Tasks API
#
@app.route('/tasks')
def tasks():
	tasks = query_db('select * from tasks')
	return JSONResponse({'items':tasks})

@app.route('/tasks', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'title': { 'type': 'string' },
			'project_id': { 'type': 'integer' }
		}
	}
)
def post_task():
	g.db.execute('insert into tasks (title, project_id, date_created) values (?, ?, current_timestamp)', (request.json['title'],request.json['project_id']))
	task_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return JSONResponse({'result':task_id}, 201)

@app.route('/tasks/<task_id>')
def task(task_id):
	tasks = query_db('select * from tasks where id=?', task_id)
	if len(tasks) == 0:
		return abort(404)
	return JSONResponse(tasks[0])

@app.route('/tasks/<task_id>', methods=['PUT'])
def put_task(task_id):
	exists = g.db.execute('select exists(select * from tasks where id=?)', (task_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('update tasks set title=?, project_id=? where id=?', (request.json['title'], request.json['project_id'], task_id))
	g.db.commit()
	tasks = query_db('select * from tasks where id=?', task_id)
	return Response('', 204)

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
	exists = g.db.execute('select exists(select * from tasks where id=?)', (task_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('delete from tasks where id=?', (task_id,))
	g.db.commit()
	return Response('', 204)

@app.route('/tasks/<task_id>/notes')
def task_notes(task_id):
	notes = query_db('select * from notes where task_id=?', task_id)
	return JSONResponse({'items':notes})


#
# Notes API
#
@app.route('/notes')
def notes():
	notes = query_db('select * from notes')
	return JSONResponse({'items':notes})

@app.route('/notes', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'text': { 'type': 'string' },
			'task_id': { 'type': 'integer' }
		}
	}
)
def post_note():
	g.db.execute('insert into notes (text, task_id) values (?, ?)', (request.json['text'],request.json['task_id']))
	task_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return JSONResponse({'result':task_id}, 201)

@app.route('/notes/<note_id>')
def note(note_id):
	notes = query_db('select * from notes where id=?', note_id)
	if len(notes) == 0:
		return abort(404)
	return JSONResponse(notes[0])

@app.route('/notes/<note_id>', methods=['PUT'])
def put_note(note_id):
	exists = g.db.execute('select exists(select * from notes where id=?)', (note_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('update notes set text=? where id=?', (request.json['text'], note_id))
	g.db.commit()
	notes = query_db('select * from notes where id=?', note_id)
	return Response('', 204)

@app.route('/notes/<note_id>', methods=['DELETE'])
def delete_note(note_id):
	exists = g.db.execute('select exists(select * from notes where id=?)', (note_id,)).fetchone()[0]
	if not exists:
		return abort(404)
	g.db.execute('delete from notes where id=?', (note_id,))
	g.db.commit()
	return Response('', 204)


#
# Users API
#
@app.route('/users', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'username': {'type': 'string'},
			'password': {'type': 'string'}
		}
	}
)
def post_user():
	g.db.execute('insert into users (username, password) values (?, ?)', (request.json['username'], request.json['password']))
	user_id = g.db.execute('select last_insert_rowid()').fetchone()[0]
	g.db.commit()
	return JSONResponse({'result':user_id}, 201)


#
# Sessions API
#
@app.route('/sessions', methods=['POST'])
@json_validate(
	{
		'type': 'object',
		'additionalProperties': False,
		'properties': {
			'username': {'type': 'string'},
			'password': {'type': 'string'}
		}
	}
)
def post_session():
	user = query_db('select * from users where username=?', request.json['username'])[0]
	if request.json['password'] == user['password']:
		response = Response()
		response.set_cookie('session', user['id'])
		return response
	return JSONResponse({'errors': ['Invalid username or password']}, 400)

@app.route('/sessions/<session_id>', methods=['DELETE'])
@require_login
def delete_session(session_id):
	print request.cookies['session']
	response = Response()
	response.set_cookie('session', 'invalid')
	return response

if __name__ == '__main__':
	app.run(debug=True)

