CREATE TABLE enigmes (
	name VARCHAR(255) PRIMARY KEY,
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

INSERT INTO teams VALUES ("Sans Team");