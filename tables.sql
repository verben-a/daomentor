create table users ( id serial PRIMARY KEY, 
	email varchar(128) unique not null, 
	password varchar(128) not null, 
	is_mentor boolean default false);

create table profiles ( id serial PRIMARY KEY,
	user_id integer references users(id),
	name_surname varchar(100) not null,
	summary varchar(255) not null,
	position_at_company varchar(255) not null,
	location varchar(100) not null,
	photo varchar(255),
	linkedin varchar(255),
	facebook varchar(255)
	);

create table experiences (id serial PRIMARY KEY,
	company_name varchar(255),
	position_name varchar(100),
	position_summary varchar(255),
	profile_id integer references profiles(id));

create table educations (id serial PRIMARY KEY,
	university_name varchar(255),
	major_name varchar(100),
	education_summary varchar(255),
	profile_id integer references profiles(id));

create table languages (id serial PRIMARY KEY,
	language_name varchar(100),
	profile_id integer references profiles(id));


create table skills (id serial PRIMARY KEY,
	skill_name varchar(100),
	profile_id integer references profiles(id));

create table services (id serial PRIMARY KEY,
	service_name varchar(255),
	cost float,
	profile_id integer references profiles(id));


# CREATE SEQUENCE user_id_seq START 101;

# CREATE SEQUENCE profile_id_seq START 101;

# CREATE SEQUENCE experience_id_seq START 101;

# CREATE SEQUENCE language_id_seq START 101;

# CREATE SEQUENCE edu_id_seq START 101;

# CREATE SEQUENCE skill_id_seq START;

# CREATE SEQUENCE skill_id_seq START 101;

# CREATE SEQUENCE service_id_seq START 101;
