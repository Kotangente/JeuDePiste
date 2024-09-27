from os import environ as env
from flask import render_template_string


INCORRECT_PASSWORD = 1
ERROR = {
	INCORRECT_PASSWORD: "password incorrect"
}

def render(path: str, **kwargs):
	template_path = env["TEMPLATE_PATH"]
	file_content = open(template_path+path, "r").read()
	return render_template_string(file_content, **kwargs)


def verify_login(cookies: dict[str, str], password: str):
	return cookies.get("LeChantDuKotangente") == password


def file_content(path: str) -> bytes:
	return open(path, "r+b").read()
