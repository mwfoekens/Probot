# Probot

### Distributed Parallelisation for [Robot Framework](https://robotframework.org/)

This project is a graduation project, and mostly a proof of concept. This project requires a lot more time before being
fully functional for all Robot Framework users. This project works on Docker as well as locally.

Install requirements:<br>
```pip install -r requirements.txt```<br><br>
This project assumes Docker and RabbitMQ (+ Erlang) are installed.

To run the project example:
<ol>
<li>Run main.py, this puts some test cases in the queue.</li>
<li>Run the docker-compose.yml to run RabbitMQ and the consumers. Consumer containers may have to be restarted as they 
can try to connect to the RabbitMQ container before it is ready.</li>
</ol>