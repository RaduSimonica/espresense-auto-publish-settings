FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
COPY app.py .
RUN pip install --no-cache-dir -r requirements.txt

# Set entry point to run the app
ENTRYPOINT ["python", "app.py"]
