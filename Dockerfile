FROM python:3.6

WORKDIR /app

COPY . /app

RUN pip install -r requeriment.txt

EXPOSE 5000

ENTRYPOINT [ "python" ]

CMD [ "main.py" ]