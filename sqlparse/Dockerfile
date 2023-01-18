FROM python:3.9.12
WORKDIR /app
RUN apt-get update -y
RUN apt-get install libecpg-dev -y
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt
COPY app/*.py /app/
ADD app/templates/ /app/templates/
ADD app/static/ /app/static/
CMD ["python","/app/server.py"]
