FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

RUN pip install uvicorn

RUN playwright install

RUN playwright install-deps

CMD ["uvicorn", "main:app", "--port", "8016", "--host", "0.0.0.0"]
