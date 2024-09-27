from os import environ as env

from flask import Flask, request, make_response, redirect, url_for
from dotenv import load_dotenv

from database import DB
from utils import render, verify_login, ERROR, INCORRECT_PASSWORD


app = Flask(__name__)
load_dotenv()

secret_url = env["SECRET_URL"]
admin_password = env["ADMIN_PASSWORD"]
assets_path = env["ASSETS_PATH"]
static_path = env["STATIC_PATH"]
database_path = env["DATABASE_PATH"]

db = DB(database_path)
hashed_password = str(hash(admin_password))


@app.get("/")
def root():
	return redirect("index.html")


@app.get(secret_url)
def admin_access():
	error = ERROR.get(int(request.args.get("error", "")), "")
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
	resp = make_response(redirect(url_for("root")))
	resp.set_cookie("LeChantDuKotangente", hashed_password)
	return resp


@app.get("/assets/<path:subpath>")
def get_asset(subpath):
	f = open(f"{assets_path}/{subpath}")
	content = f.read()
	f.close()

	return content


@app.get("/<path:subpath>")
def get_static(subpath):
	f = open(f"{static_path}/{subpath}")
	content = f.read()
	f.close()

	return content


@app.get("/enigme/<string:name>/question")
def enigme(name):
	return render("enigme.html", name=name)


@app.post("/enigme/<string:name>/answer")
def answer(name):
	return "<h3>%s</h3>" % str(list(request.form))