FROM python:3.12-slim

WORKDIR /app

# Zainstalowanie brakujących zależności systemowych
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
COPY shoplist-key.json /app/shoplist-key.json

RUN pip install --no-cache-dir -r requirements.txt

COPY src/mysite mysite

EXPOSE 5000

CMD ["uvicorn", "mysite.main:app", "--host", "0.0.0.0", "--port", "5000"]
