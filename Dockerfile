FROM python:buster

RUN pip install requests
RUN pip install bs4
RUN pip install epub_meta
RUN pip install schedule

WORKDIR /var/zeit-on-tolino/

RUN git clone https://github.com/hzulla/tolino-python.git
RUN mv tolino-python tolinoPython

COPY ./src /var/zeit-on-tolino/

ENV PYTHONUNBUFFERED 1

CMD [ "python", "./main.py" ]