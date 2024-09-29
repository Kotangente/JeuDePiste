import sqlite3


class DB:
	def __init__(self, db_path):
		self.connection = sqlite3.connect(db_path)
		self.cursor = self.connection.cursor()

	def add_enigme(self, name: str, input_type: str, question: str="", answer: str="", success: str=""):
		self.cursor.execute("""
			INSERT INTO enigmes (name, input_type, question, answer, success_message)
			VALUES (?, ?, ?, ?, ?)
		""", (name, input_type, question, answer, success))

		self.connection.commit()

	def get_enigme(self, name: str) -> tuple:
		res = self.cursor.execute("""
			SELECT input_type, question, answer, success_message
			FROM enigmes
			WHERE name = ?
		""", (name,))
		return res.fetchone()

	def get_enigmes(self) -> list[tuple]:
		res = self.cursor.execute("SELECT name FROM teams")
		return [elem[0] for elem in res.fetchall()]

	def add_answer(self, team_name: str, enigme: str, answer: str, time: int):
		if team_name not in self.get_teams():
			raise sqlite3.DataError("team '%s' doesn't exist" % team_name)
		elif self.get_enigme(enigme) is None:
			raise sqlite3.DataError("enigme '%s' doesn't exist" % enigme)

		self.cursor.execute("""
			INSERT INTO reponses (team, enigme, answer, time)
			VALUES (?, ?, ?, ?)
		""", (team_name, enigme, answer, time))

		self.connection.commit()

	def add_team(self, team_name: str):
		self.cursor.execute("INSERT INTO teams VALUES (?)", (team_name,))
		self.connection.commit()

	def get_teams(self) -> list[str]:
		res = self.cursor.execute("SELECT name FROM teams")
		return [elem[0] for elem in res.fetchall()]
	
	def get_answers_from_team(self, team: str) -> list[tuple[str, str, str]]:
		res = self.cursor.execute("""
			SELECT enigme, answer, time
			FROM reponses
			WHERE team = ?
		""", (team,))

		return res.fetchall()
	
	def get_answers_from_enigme(self, enigme: str) -> list[tuple[str, str, str]]:
		res = self.cursor.execute("""
			SELECT team, answer, time
			FROM reponses
			WHERE enigme = ?
		""", (enigme,))

		return res.fetchall()


def db_placeholder_populate(db: DB):
	enigmes = ["UN", "DEUX", "TROIS", "QUATRE"]
	teams = ["Migra", "Kotangente", "Linux", "Electro", "quoicoubeh"]

	for enigme in enigmes:
		db.add_enigme(enigme, "text", f"{enigme}???", "42", "KOTANBRAVO")

	for team in teams:
		db.add_team(team)

	for team in teams:
		for enigme in enigmes:
			answer = f"{team}: {enigme}"
			time = hash(answer)
			if time % 2 == 0:
				db.add_answer(team, enigme, answer, time)


if __name__ == "__main__":
	from os import environ as env
	from dotenv import load_dotenv

	load_dotenv()
	database_path = env["DATABASE_PATH"]

	db = DB(database_path)

	# db_placeholder_populate(db)

	# print(db.get_teams())

	# print(db.get_answers_from_team("Migra"))
	# print(db.get_answers_from_team("quoicoubeh"))
	# print(db.get_answers_from_team("Kotangente"))

	# print(db.get_answers_from_enigme("quatre"))
	# print(db.get_answers_from_enigme("quatree"))

	print(db.get_enigme("UN"))