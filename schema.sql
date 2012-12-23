create table users (
	id integer primary key,
	username text,
	password text,
	company_id integer,
	foreign key(company_id) references companies(id)
);

create table companies (
	id integer primary key,
	name text
);

create table projects (
	id integer primary key,
	name text,
	company_id integer,
	foreign key(company_id) references companies(id)
);

create table tasks (
	id integer primary key,
	title text,
	date_created date,
	date_due date,
	date_completed date,
	complete boolean,
	owner_id integer,
	project_id integer,
	foreign key(owner_id) references users(id),
	foreign key(project_id) references projects(id)
);

create table notes (
	id integer primary key,
	text text,
	task_id integer,
	foreign key(task_id) references task(id)
);
