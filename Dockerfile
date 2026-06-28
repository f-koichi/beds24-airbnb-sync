FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python generate_ics.py
EXPOSE 8080
CMD ["python", "auto_update.py"]
