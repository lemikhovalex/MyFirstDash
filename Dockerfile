FROM ubuntu:latest
MAINTAINER Aleksandr Lemikhov 'lemikhovalex@gmail.com'
RUN apt-get update -y
RUN apt-get install -y python3-pip
RUN apt-get install -y python3-dev build-essential
EXPOSE 8080
COPY . /app
WORKDIR /app 
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3"]
CMD ["main.py"]