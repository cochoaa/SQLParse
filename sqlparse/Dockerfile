from python:3.9.12
WORKDIR /app
COPY python_requeriments.txt .
RUN pip install --no-cache-dir -r python_requeriments.txt
COPY main.py .
CMD ["python","/app/main.py"]
