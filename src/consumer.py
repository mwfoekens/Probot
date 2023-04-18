import pika
import json
import os
import executor


def connect_to_receiving_channel(connection, queue):
    """
    Connecting to a channel
    :param connection:
    :param queue:
    :return: channel
    """
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    return channel


def callback(ch, method, properties, body):
    """
    This method is called every time a message is received. This method deals with test cases and then acknowledges
    :param ch:
    :param method:
    :param properties:
    :param body:
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
    # time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def channel_consume(channel, queue):
    """
    Start consuming from the channel
    :param channel:
    :param queue:
    :return: None
    """
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def start():
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
