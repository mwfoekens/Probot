import pika
import json
import os
import executor


def connect_to_receiving_channel(connection: pika.BlockingConnection, queue: str):
    """
    Connecting to a channel
    :param connection:  Connection
    :param queue:       Name of the queue
    :return: channel
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
    :return:
    """
    print(" [x] Received %r" % body.decode())
    data = json.loads(body.decode())

    try:
        # docker
        test_suite = os.environ["EXECUTOR"]
        output_location = "test-output"
    except KeyError:
        # local test
        test_suite = "LOCAL TEST"
        output_location = "log-combiner/test-output"

    executor.prepare(data, output_location, test_suite)
    executor.COUNT += 1

    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def channel_consume(channel: pika.BlockingConnection.channel, queue: str) -> None:
    """
    Start consuming from the channel
    :param channel: channel
    :param queue:   queue name
    :return:
    """
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def start() -> None:
    """
    Start the connection
    :return: None
    """
    try:
        # docker
        amqp_url = os.environ['AMQP_URL']
        queue = os.environ['QUEUE_NAME']
        url = pika.URLParameters(amqp_url)
        print("Running on Docker \nURL: " + amqp_url + "\nqueue: " + queue)
    except KeyError:
        # local test
        amqp_url = 'localhost'
        queue = 'probot_queue'
        url = pika.ConnectionParameters(amqp_url)
        print("Running locally \nURL: " + amqp_url + "\nqueue: " + queue)

    connection = pika.BlockingConnection(url)
    try:
        channel = connect_to_receiving_channel(connection, queue)
        channel_consume(channel, queue)
    except KeyboardInterrupt:
        connection.close(reply_text="Process stopped")


start()
