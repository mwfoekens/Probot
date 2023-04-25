# Probot

### Distributed Parallelisation for [Robot Framework](https://robotframework.org/)

This project is a graduation project, and mostly a proof of concept. This project requires a lot more time before being
fully functional for all Robot Framework users. This project works on Docker as well as locally. As of right now,
[Robot Framework Browser](https://robotframework-browser.org/) tests run in this example.

Install requirements:<br>
```pip install -r requirements.txt```<br><br>
This project assumes Python, Docker Desktop and RabbitMQ (+ Erlang) are installed.

To run the project example:

- Start the RabbitMQ container.
- Run main.py with arguments (run ```main.py --help``` for help).
- Run ```docker-compose.yml``` to start the consumers. Consumer containers may have to be restarted if they are started
  before
  the RabbitMQ container is started up.
- When all messages have been consumed, start the log combiner container.
    - The log combiner will output in your local directory.

## Running Containers in Kubernetes

#### When running Kubernetes, make sure to turn on Kubernetes in Docker Desktop.

* In the ```k8s-yaml``` folder, run:
    * ```kubectl apply -f .```
    * ```kubectl get service```

* Note the port number next to 5672. This will allow you to connect to RabbitMQ locally.
    * The port number next to 15672 will allow you to connect to the RabbitMQ management
      site ```localhost:<port number>```
* Pass this port with your main function so you can send clusters to the queue.
