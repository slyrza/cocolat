FROM alpine:latest

RUN apk add --no-cache bash curl wget unzip python3 py3-pip

COPY install.sh /app/install.sh
COPY bot.py /app/bot.py
WORKDIR /app

RUN chmod +x /app/install.sh && /app/install.sh

CMD ["python3", "/app/bot.py"]
