# Probot

### Distributed Parallelisation for [Robot Framework](https://robotframework.org/)

## Table of Contents

1. [Run Locally](#run-example-locally)
2. [Run with Docker Compose](#run-example-with-docker-compose)
3. [Run with Kubernetes](#run-example-with-kubernetes)
4. [Serving output with NGINX](#serving-output-files-with-nginx)
    1. [Docker Compose](#docker-compose)
    2. [Kubernetes](#kubernetes)

This project is a graduation project, and mostly a proof of concept. This project requires a lot more time before being
fully functional for all Robot Framework users. This project can run on Kubernetes & Docker, Docker Compose & Locally.
As of right now, [Robot Framework Browser](https://robotframework-browser.org/) tests can run in this example.

Install requirements:<br>

```commandline
pip install -r requirements.txt
```

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

* Ensure that ```log-combiner-pod.yaml```, ```rabbitmq-deployment.yaml``` and ```probot-consumer-deployment.yaml``` in
  the ```k8s-yaml``` folder have the correct mount paths.
* In the ```k8s-yaml``` folder, run:
    * ```kubectl apply -f .```

* To connect to RabbitMQ's AMPQ locally, use port ```32000```
    * To connect to the RabbitMQ management site use port ```31000```
    * These ports can be changed in ```rabbitmq-service.yaml```
* Pass this port with your main function so you can send clusters to the queue.

## Serving output files with NGINX

Rather getting all files returned locally, it is possible to very simply serve the results on an NGINX webserver.

### Docker Compose

In the ```docker-compose.yml```, change ```OUTPUT VOLUME``` to the name of your output volume.

```yaml
- ./OUTPUT VOLUME/:/output/
```

More information on how
to create and manage volumes in the [Docker Volumes documentation](https://docs.docker.com/storage/volumes/).

Add this to ```docker-compose.yml```:

```yaml
  nginx:
    container_name: nginx
    image: nginx:latest
    volumes:
      # configuration file
      - ./default.conf:/etc/nginx/conf.d/default.conf
      # location of logfiles
      - ./OUTPUT VOLUME/:/usr/share/nginx/html:ro
    ports:
      - "8080:80"
  ```

Create a configuration file called ```default.conf```, with the following content:

```shell
server {
    listen       80;
    listen  [::]:80;
    server_name  localhost;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
        autoindex on;
    }

    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }
}
```

The most important part is the ```autoindex on;``` line, which will generate a homepage with all output files.

### Kubernetes

Add the same default.conf file as shown in the [Docker Compose](#docker-compose) section. Mount the default.conf to your
deployment, and make sure that ```log-combiner-pod.yaml``` outputs in
your ```output-location persistent volume claim```.

Create an ```nginx-service.yaml```:

```yaml
apiVersion: v1
kind: Service
metadata:
  labels:
    io.kompose.service: nginx
  name: nginx
spec:
  ports:
    - name: "8080"
      port: 8080
      targetPort: 80
      nodePort: 30000
  selector:
    io.kompose.service: nginx
status:
  loadBalancer: { }
```

Create an ```nginx-deployment.yaml```:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  labels:
    io.kompose.service: nginx
  name: nginx
spec:
  replicas: 1
  selector:
    matchLabels:
      io.kompose.service: nginx
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        io.kompose.network/downloads-default: "true"
        io.kompose.service: nginx
    spec:
      containers:
        - image: nginx:latest
          name: nginx
          ports:
            - containerPort: 80
          resources: { }
          volumeMounts:
            - mountPath: /output-location
              name: output-location
            - mountPath: /default.conf
              name: nginx-configuration-file
      restartPolicy: Always
      volumes:
        - name: output-location
          persistentVolumeClaim:
            claimName: output-location
        - name: nginx-configuration-file
          hostPath:
            path: /run/desktop/mnt/host/c/users/YOUR PATH/default.conf
status: { }
```

And a volume for your output:

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  labels:
    io.kompose.service: output-location
  name: output-location
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 100Mi
status: { }

```