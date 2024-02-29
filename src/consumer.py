from pika.exceptions import AMQPConnectionError
import pika
import json
import os
import executor
import uuid
import time
from pathlib import Path


def on_message(ch: pika.BlockingConnection.channel, method: pika.spec.Basic.Deliver, body: bytes) -> None:
    """
    This method is called every time a message is received. This method deals with test cases and then acknowledges
    :param ch:          channel
    :param method:      method
    :param body:        message body
    :return:            None
    """
    decoded_body = body.decode()
    print(" [x] Received %r" % decoded_body)
    data: list = json.loads(decoded_body)

    executor.prepare_and_execute(data, OUTPUT_LOCATION, TEST_SUITE_PREFIX)
    executor.COUNT += 1

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consuming(channel: pika.BlockingConnection.channel, queue_name: str, timeout: int) -> int:
    """
    Start consuming messages from the queue. Times out after receiving a first message.
    :param channel:     Name of the channel
    :param queue_name:  Name of the queue
    :param timeout:     Inactivity timeout. Ensures the consumer stops when it receives nothing for a while.
    :return:            The amount of time waited
    """
    first_message_received: bool = False
    wait_time: int = 0
    for method_frame, properties, body in channel.consume(queue_name, auto_ack=False, inactivity_timeout=timeout):
        # If no first message was received, the consumer waits until a first message was received. Only when a
        # single message has been received then the consumer is allowed to stop.
        if body is None:
            if first_message_received:
                break
            else:
                wait_time += timeout
        else:
            on_message(channel, method_frame, body)
            first_message_received = True

    return wait_time


def print_divider():
    print("==============================================================================")


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
            test_suite_prefix: str = f"{test_suite_prefix} {str(uuid.uuid4())}"
            conf = "Kubernetes"

    except KeyError:
        # local test
        amqp_url: str = 'localhost'
        queue_name: str = 'probot_queue'
        connection_url: pika.ConnectionParameters = pika.ConnectionParameters(amqp_url)
        test_suite_prefix: str = f"LOCAL TEST {str(uuid.uuid4())}"
        timeout: int = 5
        output_location: str = "logcombiner/test-output"
        conf = "Local PC"

    print_divider()
    print(f"Running on {conf}\nURL:\t\t{amqp_url}\nQueue name:\t{queue_name}\nExecutor:\t{test_suite_prefix}")
    print_divider()

    return queue_name, connection_url, test_suite_prefix, output_location, timeout


def write_runtime_to_txt(output_location: str, test_suite_prefix: str, consumer_runtime: float) -> None:
    """
    Write the runtime to a txt file.
    :param output_location:     Where to store the txt
    :param test_suite_prefix:   Name of the consumer
    :param consumer_runtime:    Runtime.
    :return:                    None
    """
    with open(Path(f"{output_location}/{test_suite_prefix}-runtime.txt"), "w") as f:
        f.write(f"{consumer_runtime}")


def start(queue_name: str, connection_url: pika.URLParameters or pika.ConnectionParameters, timeout: int) -> int:
    """
    Start the connection
    :param queue_name:      Name of the queue
    :param connection_url:  URL
    :param timeout:         Inactivity timeout
    :return:                The time that was waited before the first message was received.
                            This time is not counted towards the time it took to run the tests
    """
    try:
        connection: pika.BlockingConnection = pika.BlockingConnection(connection_url)
        channel = connection.channel()

        channel.queue_declare(queue=queue_name, durable=True)
        print(' [*] Waiting for messages...')
        channel.basic_qos(prefetch_count=1)
        wait_time = start_consuming(channel, queue_name, timeout)

        channel.close()
        connection.close()
        return wait_time

    except AMQPConnectionError as e:
        print("Could not connect to queue.")
        print(f"Args: {e.args}")


if __name__ == '__main__':
    queue, url, TEST_SUITE_PREFIX, OUTPUT_LOCATION, inactivity_timeout = init()

    start_time = time.time()
    waited_time = start(queue, url, inactivity_timeout)
    end_time = time.time()
    runtime = end_time - start_time - inactivity_timeout - waited_time

    write_runtime_to_txt(OUTPUT_LOCATION, TEST_SUITE_PREFIX, runtime)

    print_divider()
    print(f"Consumer {TEST_SUITE_PREFIX} ran for {runtime} seconds.\n"
          f"Saved in {OUTPUT_LOCATION}/{TEST_SUITE_PREFIX}-runtime.txt")
    print_divider()
