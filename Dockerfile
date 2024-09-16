FROM python:3.12-slim

RUN apt update -y && \
    apt install -y git python3-pip

RUN git clone https://github.com/GreedSempai/hrBot /hrBot

WORKDIR /hrBot

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 2005

CMD ["python3.12", "./main.py"]
