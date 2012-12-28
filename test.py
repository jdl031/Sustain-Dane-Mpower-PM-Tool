import unittest
import tempfile
import app
import sqlite3
import os
import json

class SustainDaneTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()
        sqlite3.connect(app.app.config['DATABASE']).executescript(open('schema.sql').read())

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])

    def test_companies_empty(self):
        r = self.app.get('/companies')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), {"items":[]})

    def test_post_company(self):
        r = self.app.post('/companies', data='{"name":"test"}', content_type='application/json')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"result":1})

    def test_projects_empty(self):
        r = self.app.get('/projects')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), {"items":[]})

    def test_post_project(self):
        r = self.app.post('/projects', data='{"name":"test", "company_id": 1}', content_type='application/json')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"result":1})

    def test_tasks_empty(self):
        r = self.app.get('/tasks')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), {"items":[]})

    def test_post_task(self):
        r = self.app.post('/tasks', data='{"title":"test", "project_id": 1}', content_type='application/json')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"result":1})

    def test_notes_empty(self):
        r = self.app.get('/notes')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(json.loads(r.data), {"items":[]})

    def test_post_note(self):
        r = self.app.post('/notes', data='{"text": "test", "task_id": 1}', content_type='application/json')
        self.assertEqual(r.content_type, 'application/json')
        self.assertEqual(r.status_code, 201)
        self.assertEqual(json.loads(r.data), {"result":1})

if __name__ == '__main__':
	unittest.main()
