from os import environ as env
from hashlib import sha256

from flask import Flask, request, make_response, redirect, url_for, g
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import database as DB
import enigmes
from utils import render, verify_login, file_content, get_team, ERROR, INCORRECT_PASSWORD


app = Flask(__name__)
load_dotenv()

secret_url = env["SECRET_URL"]
admin_password = env["ADMIN_PASSWORD"]
static_path = env["STATIC_PATH"]
templates_path = env["TEMPLATE_PATH"]
data_path = env["DATABASE_PATH"]
db_path = data_path+"data.db"

hashed_password = sha256(bytes(admin_password, "utf-8")).hexdigest()


@app.teardown_appcontext
def close_connection(exception):
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()


@app.get("/")
def root():
	return get_static("/")


@app.get(secret_url)
def admin_access():
	error = ERROR.get(int(request.args.get("error", 0)), "")
	return f"""
	<form action="{secret_url}/login" method="POST">
		<label for="password">Enter Admin Password:</label><br>
		<input type="password" name="password" placeholder="password">
		<input type="submit" value="enter">
	</form>
	<p id="error-message">{error}</p>
"""


@app.post(f"{secret_url}/login")
def login():
	if request.form.get("password") != admin_password:
		return redirect(url_for("admin_access")+"?error=%d"%INCORRECT_PASSWORD)
	resp = make_response(redirect(url_for("admin")))
	resp.set_cookie("LeChantDuKotangente", hashed_password)
	return resp


@app.get("/checkadmin")
def check_admin():
	if verify_login(request.cookies, hashed_password):
		return """
		Askip t'es admin! tu peux accéder à ton espace admin <a href=/admin>juste ici</a>!
		"""
	else:
		return ""


@app.get("/admin/")
@app.get("/admin/<path:subpath>")
def admin(subpath=""):
	if not verify_login(request.cookies, hashed_password):
		return redirect(url_for("root"))
	return get_static("/admin/" + subpath)


@app.get("/<path:subpath>")
def get_static(subpath):
	path = f"{static_path}{subpath}"
	try:
		return file_content(path)
	except IsADirectoryError:
		return file_content(path.removesuffix("/") + "/index.html")


@app.post("/enigme/create")
def create_enigme():
	if not verify_login(request.cookies, hashed_password):
		redirect(url_for("root"))

	return enigmes.create(request)


@app.get("/enigme/<string:id>")
def get_enigme(id):
	return enigmes.get(id)


@app.post("/enigme/<string:id>/answer")
def answer_enigme(id):
	enigme = enigmes.get_name(id)
	team = get_team(request.cookies)
	if enigmes.answered_enigme(team, enigme)\
			or enigmes.in_fail_state(team, enigme) > 0.0:
		return status_enigme(id)
	return enigmes.answer(id, request)


@app.get("/enigme/<string:id>/status")
def status_enigme(id):
	team = get_team(request.cookies)
	enigme = enigmes.get_name(id)
	if enigmes.answered_enigme(team, enigme):
		return "<div class='correct'>Vous avez déjà résolu cette énigme</div>"
	elif (t := enigmes.in_fail_state(team, enigme)) > 0.0:
		return f"""
			<div class='incorrect'
				hx-trigger='every 1s'
				hx-get='/enigme/{id}/status'
				hx-swap='innerHTML'>
				Vous pouvez réessayer dans {int(t)} secondes.
			</div>
		"""
	else:
		print(t)
		return ""


@app.get("/infos/enigmes")
def get_enigmes():
	return "".join([f"""
		<tr>
			<td>
				<a href='{url_for('enigme_data_page', id=enigmes.get_id(enigme))}'>{enigme}</a>
			</td>
			<td>
				<button hx-delete='/enigme/{enigmes.get_id(enigme)}'
						hx-confirm='Supprimer l'énigme \"{enigme}\"?'>
					delete
				</button>
			</td>
		</tr>
		"""
		for enigme in DB.get_enigmes()])


@app.get("/infos/teams")
def get_teams():
	return "".join([f"<li><a href='{url_for('team_data_page', name=team)}'>{team}</a></li>"
				 for team in DB.get_teams()])


@app.get("/admin/enigmes/<string:id>")
def enigme_data_page(id):
	return render("infos.html", name=enigmes.get_name(id), id=id, type="enigmes")


@app.get("/admin/teams/<string:name>")
def team_data_page(name):
	return render("infos.html", name=name, id=name, type="teams", team=True)


@app.get("/infos/enigmes/<string:id>")
def get_enigme_data(id):
	return enigmes.render_table_enigmes(id)


@app.get("/infos/teams/<string:name>")
def get_team_data(name):
	return enigmes.render_table_team(name)


@app.delete("/enigme/<string:id>")
def delete_enigme(id):
	DB.delete_enigme(id)


@app.get("/data/images/<path:subpath>")
def get_image(subpath):
	return file_content(data_path+"images/"+secure_filename(subpath))


@app.post("/team")
def choose_team():
	team = request.form.get("team")
	DB.add_team(team)
	
	resp = make_response("ok!!")
	resp.set_cookie("team", team)
	return resp