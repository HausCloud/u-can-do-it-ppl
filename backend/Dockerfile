FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "app:fastapi", "--host", "0.0.0.0"]