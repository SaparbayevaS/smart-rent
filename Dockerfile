FROM python:3.13

WORKDIR /app

COPY  requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
