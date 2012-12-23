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

	[Notes on Functions]
	--------------------
	/Projects/							POST: Create Project, GET: List of Projects, DELETE: N/A
	/Projects/<projectID>				POST: Edit, GET: Overview of single project, DELETE: Remove project
	/Projects/<projectID>/Tasks/		POST: Create Task, GET: List of Tasks under project, DELETE: N/A
	...
	/Users/<userID>/Tasks				GET: List of user's tasks


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
