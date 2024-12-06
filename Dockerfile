FROM python:3.8
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

RUN mkdir -p /var/www/app/

WORKDIR /var/www/app/

COPY . /var/www/app/

RUN cd /var/www/app/

RUN pip install -r requirements.txt

ENV DATABASE_URL=${DATABASE_URL}
#ENV FLASK_APP app.py
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]