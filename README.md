# Probot

### Distributed Parallelisation for [Robot Framework](https://robotframework.org/)

This project is a graduation project, and mostly a proof of concept. This project requires a lot more time before being
fully functional for all Robot Framework users. This project works on Docker as well as locally. As of right now,
[Robot Framework Browser](https://robotframework-browser.org/) tests run in this example.

Install requirements:<br>
```pip install -r requirements.txt```<br><br>
This project assumes Python, Docker and RabbitMQ (+ Erlang) are installed.

To run the project example:
<ol>
<li>Start the RabbitMQ container.</li>
<li>Run main.py, this puts some test cases in the queue.</li>
<li>Run the docker-compose.yml to the consumers. Consumer containers may have to be restarted if they are started before
the RabbitMQ container is started up.</li>
<li>When all messages have been consumed, start the log combiner container.</li>
</ol>