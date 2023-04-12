FROM python:latest
ENV PYTHONUNBUFFERED=1
WORKDIR /data
RUN git clone https://github.com/mwfoekens/Probot data/app
WORKDIR /data/app
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install -r /tmp/requirements.txt
COPY consumer.py .
COPY data_preparer.py .
CMD ["python", "/data/app/consumer.py"]