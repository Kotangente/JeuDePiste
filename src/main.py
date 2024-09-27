from os import environ as env

from flask import Flask, request, make_response, redirect, url_for, render_template_string
from dotenv import load_dotenv
from Crypto.Cipher import AES
import sqlite3


app = Flask(__name__)
load_dotenv()

secret_url = env["SECRET_URL"]
admin_password = env["ADMIN_PASSWORD"]
crypt_key = bytes(env["ENCRYPTION_KEY"], "utf-8")
assets_path = env["ASSETS_PATH"]
static_path = env["STATIC_PATH"]
database_path = env["DATABASE_PATH"]

database_connection = sqlite3.connect(database_path)


@app.get("/")
def root():
	return redirect("index.html")


@app.get(secret_url)
def admin_access():
	return '''
	<form action="/login" method="POST">
		<label for="password">Enter Admin Password:</label><br>
		<input type="password" id="password" name="password" placeholder="password">
		<input type="submit" value="enter">
	</form>
'''


@app.post("/login")
def login():
	resp = make_response(redirect(url_for(secret_url)))
	resp.set_cookie("LeChantDuKotangente", )
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
	file_content = open("templates/enigme.html", "r").read()
	return render_template_string(file_content, name=name)


@app.post("/enigme/<string:name>/answer")
def answer(name):
	return "<h3>%s</h3>" % str(list(request.form))