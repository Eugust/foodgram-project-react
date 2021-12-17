FROM python:3.7-slim
RUN mkdir /backend
COPY requirements.txt /backend
RUN pip3 install -r /backend/requirements.txt
COPY . /backend
WORKDIR /backend
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000"]