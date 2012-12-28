TO DO
=====
* SQL Schema
* Python Functions
* Pages


Schema
======
[X] Done

Functions
=========
* SuperAdmin (person from Sustain Dane): Create Admin
* Admin: Create account
* User login - return: company ID
* Create/Edit Project (input: Company ID, Title, Created by User)   [Created by company admin]
* Create/Edit Task (input: Project, title, Created by User, Assigned to User, Due Date)  [Created by anyone (or configurable by admin settings)]
* Create/Edit Note  (input: Task, Title, Text, created by user, created date) [Created by anyone]
* Get Projects from Customer ID
* Get Tasks from Project ID
* Get Notes from Task ID
* Get Tasks from User ID (for "my tasks page")
* Mark task as complete
* Flask API unittesting
* Return createdresource url in POST 201 response
* Give all objects created, updated timestamps?
* Notifications: Task Create, Note Post (next phase)

	[API]
	--------------------
	GET     /companies 200
	POST    /companies 201
	GET     /companies/<company_id> 200, 404
	PUT     /companies/<company_id> 204, 400, 404
	DELETE  /companies/<company_id> 204, 404
	GET     /companies/<company_id>/projects 200, 404

	GET     /projects 200
	POST    /projects 201
	GET     /projects/<project_id> 200, 404
	PUT     /projects/<project_id> 204, 400, 404
	DELETE  /projects/<project_id> 204, 404
	GET     /projects/<project_id>/tasks 200, 404

	GET     /tasks 200
	POST    /tasks 201
	GET     /tasks/<task_id> 200, 404
	PUT     /tasks/<task_id> 204, 400, 404
	DELETE  /tasks/<task_id> 204, 404
	GET     /tasks/<task_id>/notes 200, 404

	GET     /notes 200
	POST    /notes 201
	GET     /notes/<note_id> 200, 404
	PUT     /notes/<note_id> 204, 400, 404
	DELETE  /notes/<note_id> 204, 404

	GET     /users 200
	GET     /users/<user_id> 200, 404
	GET     /users/<user_id>/tasks 200, 404



General
=======
* Lock pages to check for authenticated session (Flask login extension module?)
* If not authenticated, redirect to login page.

Pages
=====
* Check out forms library 
* Login page
* Projects List Page
* Create Project Page
* Tasks list Page
* Create Task Page
* Notes list Page
* Create Notes Page
* My Tasks Page
* Settings Page: Create new account (admin only), subscribe to notifications (next phase)

Deployment
==========
* Set up app on Heroku
* research options for hosting under sustaindane.org domain (as opposed to blah.herokuapps.org)

Next Phase
==========
* Notifications
* ? In-line edit/create
