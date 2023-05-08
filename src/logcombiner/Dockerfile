FROM python:latest
ENV PYTHONUNBUFFERED=1
RUN mkdir "output"
RUN python3 -m pip install --upgrade pip && python3 -m pip install robotframework
COPY log_combiner.py .
CMD ["python3", "log_combiner.py"]
