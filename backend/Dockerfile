FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "app:fastapi", "--host", "0.0.0.0"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["uvicorn", "app:fastapi", "--host", "0.0.0.0", "--port", "80", "--proxy-headers"]