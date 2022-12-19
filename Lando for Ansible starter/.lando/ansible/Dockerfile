FROM python:3.11

RUN apt-get update -y \
  && apt-get install -y sshpass ansible python3-jmespath ruby python3-passlib python3-bcrypt vim nano

RUN ansible-galaxy collection install community.general

RUN pip3 install jmespath

RUN apt install mc -y
