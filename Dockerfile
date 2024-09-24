FROM python:3.12-slim

RUN apt update -y && \
    apt install -y git python3-pip

WORKDIR /bot

COPY requirements.txt .
COPY *.py .
COPY *.png .

RUN pip install -r requirements.txt

EXPOSE 3012

CMD ["python3.12", "./main.py"]
