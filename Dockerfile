FROM python:3.11-slim-bullseye

WORKDIR /app

COPY ./requirements/base.txt ./base.txt
RUN pip install --no-cache-dir --upgrade -r base.txt
COPY ./src ./src
COPY ./logs ./logs

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]