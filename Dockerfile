FROM python:3.6.12-buster

RUN apt-get update
WORKDIR /root
COPY requirements.txt /root/requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "-u", "app.py"]
