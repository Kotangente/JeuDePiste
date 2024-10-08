CREATE TABLE enigmes (
	id VARCHAR(255) PRIMARY KEY,
	name VARCHAR(255),
	input_type VARCHAR(255),
	question VARCHAR,
	answer VARCHAR,
	success_message VARCHAR
);

CREATE TABLE reponses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	team VARCHAR(255),
	enigme VARCHAR(255),
	answer VARCHAR,
	time INTEGER,
	FOREIGN KEY(team) REFERENCES teams(name),
	FOREIGN KEY(enigme) REFERENCES enigmes(name)
);

CREATE TABLE teams (
	name VARCHAR(255) PRIMARY KEY
);

CREATE TABLE fail (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	team VARCHAR(255),
	enigme VARCHAR(255),
	attempt_count INTEGER,
	time INTEGER,
	FOREIGN KEY(team) REFERENCES teams(name),
	FOREIGN KEY(enigme) REFERENCES enigmes(name)
);

INSERT INTO teams VALUES ("Sans Team");