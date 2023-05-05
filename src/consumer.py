from pika.exceptions import AMQPConnectionError
import pika
import json
import os
import executor
import uuid
import time
from pathlib import PurePath


def on_message(ch: pika.BlockingConnection.channel, method: pika.spec.Basic.Deliver,
               properties: pika.spec.BasicProperties, body: bytes) -> None:
    """
    This method is called every time a message is received. This method deals with test cases and then acknowledges
    :param ch:          channel
    :param method:      method
    :param properties:  properties
    :param body:        message body
    :return:            None
    """
    print(" [x] Received %r" % body.decode())
    data: list = json.loads(body.decode())

    executor.prepare(data, OUTPUT_LOCATION, TEST_SUITE_PREFIX)
    executor.COUNT += 1

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def init() -> tuple:
    """
    Initialise some variables when starting. Is different based on if run on Docker Compose, K8s or local.
    :return: all required variables
    """
    try:
        # docker/k8s
        amqp_url: str = os.environ['AMQP_URL']
        queue_name: str = os.environ['QUEUE_NAME']
        connection_url: pika.URLParameters = pika.URLParameters(amqp_url)
        test_suite_prefix: str = os.environ["EXECUTOR"]
        timeout: int = int(os.environ["INACTIVITY"])
        output_location: str = "test-output"

        conf = "Docker"
        if test_suite_prefix.startswith("Kubernetes"):
            test_suite_prefix: str = test_suite_prefix + str(f" {uuid.uuid4()}")
            conf = "Kubernetes"

    except KeyError:
        # local test
        amqp_url: str = 'localhost'
        queue_name: str = 'probot_queue'
        connection_url: pika.ConnectionParameters = pika.ConnectionParameters(amqp_url)
        test_suite_prefix: str = "LOCAL TEST"
        timeout: int = 5
        output_location: str = "log-combiner/test-output"
        conf = "Local PC"

    print("==============================================================================")
    print(f"Running on {conf}\nURL:\t\t{amqp_url}\nQueue name:\t{queue_name}\nExecutor:\t{test_suite_prefix}")
    print("==============================================================================")

    return queue_name, connection_url, test_suite_prefix, output_location, timeout


def write_runtime_to_txt(output_location: str, test_suite_prefix: str, consumer_runtime: float) -> None:
    """
    Write the runtime to a txt file.
    :param output_location:     Where to store the txt
    :param test_suite_prefix:   Name of the consumer
    :param consumer_runtime:             Runtime.
    :return:                    None
    """
    with open(PurePath(f"{output_location}/{test_suite_prefix}-runtime.txt"), "w") as f:
        f.write(f"{consumer_runtime}")


def start(queue_name: str, connection_url: pika.URLParameters or pika.ConnectionParameters, timeout: int) -> None:
    """
    Start the connection
    :param queue_name:              Name of the queue
    :param connection_url:                     URL
    :param timeout:      Inactivity timeout
    :return: None
    """
    try:
        connection: pika.BlockingConnection = pika.BlockingConnection(connection_url)
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        print(' [*] Waiting for messages...')
        channel.basic_qos(prefetch_count=1)
        for method_frame, properties, body in channel.consume(queue_name, auto_ack=False, inactivity_timeout=timeout):
            if body is None:
                break

            on_message(channel, method_frame, properties, body)

        channel.close()
        connection.close()

    except AMQPConnectionError as e:
        print("Could not connect to queue.")
        print(f"Args: {e.args}")


queue, url, TEST_SUITE_PREFIX, OUTPUT_LOCATION, inactivity_timeout = init()

start_time = time.time()
start(queue, url, inactivity_timeout)
runtime = time.time() - start_time - inactivity_timeout

write_runtime_to_txt(OUTPUT_LOCATION, TEST_SUITE_PREFIX, runtime)

print("==============================================================================")
print(f"Consumer {TEST_SUITE_PREFIX} ran for {runtime} seconds.\n"
      f"Saved in {OUTPUT_LOCATION}/{TEST_SUITE_PREFIX}-runtime.txt")
print("==============================================================================")
