FROM python:3.10


RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
COPY . .

EXPOSE 5000
CMD ["flask", "--app", "src/main", "run"]
