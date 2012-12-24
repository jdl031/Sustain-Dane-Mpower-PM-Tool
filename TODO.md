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
* Notifications: Task Create, Note Post (next phase)

	[API]
	--------------------
	GET     /companies
	POST    /companies
	GET     /companies/<company_id>
	PUT     /companies/<company_id>
	DELETE  /companies/<company_id>
	GET     /companies/<company_id>/projects

	GET     /projects
	POST    /projects
	GET     /projects/<project_id>
	PUT     /projects/<project_id>
	DELETE  /projects/<project_id>
	GET     /projects/<project_id>/tasks

	GET     /tasks
	POST    /tasks
	GET     /tasks/<task_id>
	PUT     /tasks/<task_id>
	DELETE  /tasks/<task_id>
	GET     /tasks/<task_id>/notes

	GET     /notes
	POST    /notes
	GET     /notes/<note_id>
	PUT     /notes/<note_id>
	DELETE  /notes/<note_id>

	GET     /users
	GET     /users/<user_id>
	GET     /users/<user_id>/tasks



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
