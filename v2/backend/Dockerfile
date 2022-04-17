FROM python:3.7-slim-buster
COPY . /app
WORKDIR /app
EXPOSE 5555
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "server.py"]
