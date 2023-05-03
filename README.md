# Probot

### Distributed Parallelisation for [Robot Framework](https://robotframework.org/)

This project is a graduation project, and mostly a proof of concept. This project requires a lot more time before being
fully functional for all Robot Framework users. This project can run on Kubernetes & Docker, Docker Compose & Locally.
As of right now, [Robot Framework Browser](https://robotframework-browser.org/) tests can run in this example.

Install requirements:<br>
```pip install -r requirements.txt```<br><br>
This project assumes Python 3.11 and Docker Desktop are installed.<br>

To generate an output.xml so the algorithm will split up tests based on execution time, run the ```.robot``` tests in
the ```suites``` folder, and pass the output.xml file location in ```main.py```.

## Run example locally

- Start a RabbitMQ container (a RabbitMQ Docker container saves work and effort).
- Run as many ```consumer.py``` instances as desired.
- Start the ```main.py``` with arguments (run ```main.py --help``` for help).

## Run example with Docker Compose

- Start the RabbitMQ container.
- Run main.py with arguments.
- Run ```docker-compose.yml``` to start the consumers. Consumer containers may have to be restarted if they are started
  before the RabbitMQ container is started up (```AMPQConnectionError```)
- When all messages have been consumed, start the ```log combiner``` container.
    - The log combiner will output in your local directory.

## Run example with Kubernetes

#### ! When running Kubernetes, make sure to turn on Kubernetes in Docker Desktop !

* Ensure that ```log-combiner-deployment.yaml```, ```rabbitmq-deployment.yaml```
  and ```probot-consumer-deployment.yaml``` in the ```k8s-yaml``` folder have the correct mount paths.
* In the ```k8s-yaml``` folder, run:
    * ```kubectl apply -f .```

* To connect to RabbitMQ's AMPQ locally, use port ```32000```
    * To connect to the RabbitMQ management site use port ```31000```
    * These ports can be changed in ```rabbitmq-service.yaml```
* Pass this port with your main function so you can send clusters to the queue.
