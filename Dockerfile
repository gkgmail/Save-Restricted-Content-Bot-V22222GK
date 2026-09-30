FROM python:3.11-slim

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y git curl wget bash ffmpeg

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -U -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["python3", "-m", "devgagan"]
