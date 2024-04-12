 FROM python:3.8.10-slim-buster
 ENV PYTHONUNBUFFERED 1
 WORKDIR /code
 COPY ./requirements.txt /code/requirements.txt
 RUN pip install pytest-runner
 RUN pip install -r requirements.txt
 COPY . /code/
 CMD ["python3", "main_predesarrollo.py", "0", "8000"]
 EXPOSE 8000
 HEALTHCHECK NONE