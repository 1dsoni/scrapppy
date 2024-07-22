FROM python:3.12

RUN mkdir /code

WORKDIR /code/

ADD requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ADD . /code/

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

CMD ["/code/web_server.sh"]