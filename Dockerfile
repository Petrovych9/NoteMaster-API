FROM python:3.12.0

ENV PYTHONBUFFERED 1

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

