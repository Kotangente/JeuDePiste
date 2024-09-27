CREATE TABLE enigmes (
	name VARCHAR PRIMARY KEY,
	input_type VARCHAR,
	image VARCHAR
);

CREATE TABLE reponses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	team VARCHAR,
	enigme VARCHAR,
	answer VARCHAR,
	time INTEGER,
	FOREIGN KEY(enigme) REFERENCES enigmes(name)
);