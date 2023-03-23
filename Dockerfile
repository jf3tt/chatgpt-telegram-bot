FROM python:3.10-slim-bullseye
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT [ "python3", "app.py" ]