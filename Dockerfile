FROM python:buster

WORKDIR /var/zeit-on-tolino/

RUN pip install requests && pip install bs4 && pip install epub_meta && pip install schedule && git clone https://github.com/darkphoenix/tolino-calibre-sync.git && mv tolino-calibre-sync tolinoPython

COPY ./src /var/zeit-on-tolino/

ENV PYTHONUNBUFFERED 1

CMD [ "python", "./main.py" ]