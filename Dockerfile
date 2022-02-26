FROM python:3.8-alpine

WORKDIR /BMG_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py",  "--host=0.0.0.0"]