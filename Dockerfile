FROM python:3.10

WORKDIR /app

COPY . /app/

RUN apt-get update && apt-get install -y ffmpeg

RUN pip3 install -r requirements.txt

CMD ["python3", "app.py"]
