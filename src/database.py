import sqlite3
from os import environ as env

from flask import g


def get_db(db_path=None):
	if db_path == None:
		db_path = env["DATABASE_PATH"]+"data.db"

	db = getattr(g, "_database", None)
	if db is None:
		db = g._database = sqlite3.connect(db_path)

	return db


def query_db(query, args=(), one=False):
	db = get_db()
	cursor = db.execute(query, args)
	res = cursor.fetchall()
	cursor.close()
	db.commit()
	return (res[0] if res else None) if one else res


def add_enigme(name: str, input_type: str, question: str="", answer: str="", success: str=""):
	query_db("""
		INSERT INTO enigmes (name, input_type, question, answer, success_message)
		VALUES (?, ?, ?, ?, ?)
	""", (name, input_type, question, answer, success))


def get_enigme(name: str) -> tuple[str, str, str, str]:
	return query_db("""
		SELECT input_type, question, answer, success_message
		FROM enigmes
		WHERE name = ?
	""", (name,), one=True)


def get_enigmes() -> list[str]:
	res = query_db("SELECT name FROM enigmes")
	return [elem[0] for elem in res]


def add_answer(team_name: str, enigme: str, answer: str, time: int):
	if team_name not in get_teams():
		raise sqlite3.DataError("team '%s' doesn't exist" % team_name)
	elif get_enigme(enigme) is None:
		raise sqlite3.DataError("enigme '%s' doesn't exist" % enigme)

	query_db("""
		INSERT INTO reponses (team, enigme, answer, time)
		VALUES (?, ?, ?, ?)
	""", (team_name, enigme, answer, time))


def add_team(team_name: str):
	query_db("INSERT INTO teams VALUES (?)", (team_name,))


def get_teams() -> list[str]:
	res = query_db("SELECT name FROM teams")
	return [elem[0] for elem in res]


def get_answers_from_team(team: str) -> list[tuple[str, str, str]]:
	return query_db("""
		SELECT enigme, answer, time
		FROM reponses
		WHERE team = ?
	""", (team,))


def get_answers_from_enigme(enigme: str) -> list[tuple[str, str, str]]:
	return query_db("""
		SELECT team, answer, time
		FROM reponses
		WHERE enigme = ?
	""", (enigme,))


def delete_enigme(enigme: str):
	query_db("""
		DELETE FROM enigmes WHERE name = ?;
	""", (enigme,))


def db_placeholder_populate():
	enigmes = ["UN", "DEUX", "TROIS", "QUATRE"]
	teams = ["Migra", "Kotangente", "Linux", "Electro", "quoicoubeh"]

	for enigme in enigmes:
		add_enigme(enigme, "text", f"{enigme}???", "42", "KOTANBRAVO")

	for team in teams:
		add_team(team)

	for team in teams:
		for enigme in enigmes:
			answer = f"{team}: {enigme}"
			time = hash(answer)
			if time % 2 == 0:
				add_answer(team, enigme, answer, time)


if __name__ == "__main__":
	from dotenv import load_dotenv

	load_dotenv()

	db = get_db()

	# db_placeholder_populate()

	# print(db.get_teams())

	# print(get_answers_from_team("Migra"))
	# print(get_answers_from_team("quoicoubeh"))
	# print(get_answers_from_team("Kotangente"))

	# print(get_answers_from_enigme("quatre"))
	# print(get_answers_from_enigme("quatree"))

	print(get_enigme("UN"))