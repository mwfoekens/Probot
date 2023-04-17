FROM python:latest
ENV PYTHONUNBUFFERED=1
#WORKDIR /data
#RUN git clone https://github.com/mwfoekens/Probot data/app
#WORKDIR /data/app
RUN mkdir "/suites"
COPY ../requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --upgrade pip && python3 -m pip install -r /tmp/requirements.txt
COPY src/consumer.py .
COPY src/executor.py .
COPY ../suites/testSuite1.robot suites
COPY ../suites/testSuite2.robot suites
CMD ["python3", "consumer.py"]