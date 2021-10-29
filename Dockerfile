FROM python:buster

WORKDIR /var/zeit-on-tolino/

RUN pip install requests && pip install bs4 && pip install epub_meta && pip install schedule && pip install cloudscraper && git clone -b issue_45 https://github.com/tobexyz/tolino-python.git && mv tolino-python tolinoPython

COPY ./src /var/zeit-on-tolino/

ENV PYTHONUNBUFFERED 1

CMD [ "python", "./main.py" ]