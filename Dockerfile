FROM python:3.12.0-slim
LABEL authors="Andrew Kyzmin"

EXPOSE 80
WORKDIR /usr/src/bot_app

COPY requires.txt ./

RUN pip install --upgrade setuptools

RUN pip install --no-cache-dir -r requires.txt

RUN chmod 755 .

COPY . .

CMD ["python3", "main.py"]