FROM python:3.10

VOLUME [ "/spider/data" ]

WORKDIR /spider

COPY . .

RUN pip install -r requirements.txt && playwright install firefox --with-deps

CMD ["python3", "spider.py"]
