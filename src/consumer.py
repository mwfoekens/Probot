from pika.exceptions import AMQPConnectionError
import pika
import json
import os
import executor
import uuid


def connect_to_receiving_channel(connection: pika.BlockingConnection, queue: str) -> pika.BlockingConnection.channel:
    """
    Connecting to a channel
    :param connection:  Connection
    :param queue:       Name of the queue
    :return:            channel
    """
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    return channel


def callback(ch: pika.BlockingConnection.channel, method: pika.spec.Basic.Deliver,
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


def channel_consume(channel: pika.BlockingConnection.channel, queue: str) -> None:
    """
    Start consuming from the channel
    :param channel: channel
    :param queue:   queue name
    :return:        None
    """
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def init() -> tuple:
    """
    Initialise some variables when starting
    :return: all required variables
    """
    try:
        # docker/k8s
        amqp_url: str = os.environ['AMQP_URL']
        queue: str = os.environ['QUEUE_NAME']
        url: pika.URLParameters = pika.URLParameters(amqp_url)
        test_suite_prefix: str = os.environ["EXECUTOR"]
        output_location: str = "test-output"

        conf = "Docker"
        if test_suite_prefix.startswith("Kubernetes"):
            test_suite_prefix: str = test_suite_prefix + str(f" {uuid.uuid4()}")
            conf = "Kubernetes"

    except KeyError:
        # local test
        amqp_url: str = 'localhost'
        queue: str = 'probot_queue'
        url: pika.ConnectionParameters = pika.ConnectionParameters(amqp_url)
        test_suite_prefix: str = "LOCAL TEST"
        output_location: str = "log-combiner/test-output"
        conf = "Local PC"

    print(f"Running on {conf} \nURL: {amqp_url}\nQueue name: {queue}\nExecutor: {test_suite_prefix}")

    return queue, url, test_suite_prefix, output_location


def start() -> None:
    """
    Start the connection
    :return: None
    """
    connection: pika.BlockingConnection = pika.BlockingConnection(URL)
    try:
        channel = connect_to_receiving_channel(connection, QUEUE)
        channel_consume(channel, QUEUE)
    except KeyboardInterrupt:
        connection.close(reply_text="Process stopped")
    except AMQPConnectionError as e:
        print("Could not connect to queue.")
        print(f"Args: {e.args}")


QUEUE, URL, TEST_SUITE_PREFIX, OUTPUT_LOCATION = init()
start()
