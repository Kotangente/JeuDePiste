from os import environ as env
import time
from datetime import datetime

from werkzeug.utils import secure_filename
from flask import Request

import database as db
from utils import render


data_path = env["DATABASE_PATH"]


def create(request: Request):
	form = request.form
	name = form.get("name")
	question = form.get("question")
	answer = form.get("answer")
	success_msg = form.get("success_msg")

	image = request.files.get("image")
	if image is not None:
		extension = image.filename.split(".")[-1]
		image.save(f"{data_path}images/enigme_{secure_filename(name)}.{extension}")

	input_type = "text"
	if answer == "":
		input_type = "none"
	elif answer.isnumeric():
		input_type = "number"
	elif answer == "%%IMAGE%%":
		input_type = "file"

	db.add_enigme(name, input_type, question, answer, success_msg)

	return "O.K.! <a href='./'>return</a>"


def get(name: str):
	input_type, question, _, _ = db.get_enigme(name)

	image = True
	try:
		f = open(data_path+"images/"+"enigme_"+secure_filename(name)+".png")
		f.close()
	except:
		image = False
	return render("enigme.html",
			name=name,
			input_type=input_type,
			question=question,
			image=image)
		

def answer(enigme: str, request: Request):
	team = request.cookies.get("team", "Sans Team")

	resp = "%%IMAGE%%"
	image = request.files.get("resp")
	if image is not None:
		ext = image.filename.split(".")[-1]
		image.save(data_path+"images/"+team.replace(" ", "_")+"_"+enigme.replace(" ", "_")+".png")
	else:
		resp = request.form.get("resp")

	_, _, correct_resp, success_msg = db.get_enigme(enigme)

	if resp == correct_resp:
		t = time.time_ns()
		db.add_answer(team, enigme, resp, t)
		return f"<div class='correct'>{success_msg}</div>"
	else:
		return "<div class='incorrect'>WRONG</div>"


def render_table_enigmes(name: str):
	data = [list(row) for row in db.get_answers_from_enigme(name)]
	data.sort(key=lambda x: x[-1])
	for row in data:
		row[-1] = str(datetime.fromtimestamp(int(row[-1])/1_000_000_000))
		if row[1] == "%%IMAGE%%":
			enigme = name.replace(" ", "_")
			team = row[0].replace(" ", "_")
			row[1] = "<img src='/data/images/"+team+"_"+enigme+".png'>"
	return render("tableau.html", header=["team", "réponse", "temps"], rows=data)


def render_table_team(name: str):
	data = [list(row) for row in db.get_answers_from_team(name)]
	data.sort(key=lambda x: int(x[-1]))
	for row in data:
		row[-1] = str(datetime.fromtimestamp(int(row[-1])/1_000_000_000))
		if row[1] == "%%IMAGE%%":
			team = name.replace(" ", "_")
			enigme = row[0].replace(" ", "_")
			row[1] = "<img src='/data/images/"+team+"_"+enigme+".png'>"
	return render("tableau.html", header=["énigme", "réponse", "temps"], rows=data)
