FROM python:3.8-alpine
ENV PYTHONUNBUFFERED=1


WORKDIR /BMG_app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "-u", "run.py",  "--host=0.0.0.0"]