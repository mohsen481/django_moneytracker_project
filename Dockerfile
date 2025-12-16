FROM python:3.13
RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python3-dev curl && rm -rf /var/lib/apt/lists/*
RUN mkdir dj_app
WORKDIR dj_app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV DB_HOST=db
CMD ["python","manage.py","runserver","0.0.0.0:8000"]