FROM python:3-slim

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN pip install -r ./requirements.txt

WORKDIR /workspace

RUN chmod -R 777 /workspace

USER 1000:1000

ENTRYPOINT [ "python", "/app/src/__main__.py" ]