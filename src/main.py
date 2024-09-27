from os import environ as env

from flask import Flask, request, make_response, redirect, url_for
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from database import DB
import enigmes
from utils import render, verify_login, file_content, ERROR, INCORRECT_PASSWORD


app = Flask(__name__)
load_dotenv()

secret_url = env["SECRET_URL"]
admin_password = env["ADMIN_PASSWORD"]
static_path = env["STATIC_PATH"]
templates_path = env["TEMPLATE_PATH"]
data_path = env["DATABASE_PATH"]
db_path = data_path+"data.db"

# hashed_password = str(hash(admin_password))
hashed_password = admin_password


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


@app.get("/admin/")
@app.get("/admin/<path:subpath>")
def admin(subpath=""):
	if not verify_login(request.cookies, hashed_password):
		return redirect(url_for("root"))
	return get_static("/admin/" + subpath)


@app.get("/<path:subpath>")
def get_static(subpath):
	path = f"{static_path}/{subpath}"
	try:
		return file_content(path)
	except IsADirectoryError:
		return file_content(path.removesuffix("/") + "/index.html")


@app.post("/enigme/create")
def create_enigme():
	if not verify_login(request.cookies, hashed_password):
		redirect(url_for("root"))

	db = DB(db_path)
	try:
		return enigmes.create(request, db)
	finally:
		db.connection.close()


@app.get("/enigme/<string:name>")
def get_enigme(name):
	db = DB(db_path)
	try:
		return enigmes.get(name, db)
	finally:
		db.connection.close()


@app.post("/enigme/<string:name>/answer")
def answer_enigme(name):
	db = DB(db_path)
	try:
		return enigmes.answer(name, request, db)
	finally:
		db.connection.close()


@app.get("/data/images/<path:subpath>")
def get_image(subpath):
	return file_content(data_path+"images/"+secure_filename(subpath))
