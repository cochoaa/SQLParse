from python:3.9.12
WORKDIR /app
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt
COPY app/*.py /app/
CMD ["python","/app/server.py"]
