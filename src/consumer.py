import pika
import time
import json
import os
import executor


def connect_to_receiving_channel(connection, queue):
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    return channel


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    data = json.loads(body.decode())

    try:
        # docker
        test_suite = os.environ["EXECUTOR"]
    except KeyError:
        # local test
        test_suite = "LOCAL TEST"

    executor.prepare(data, "log-combiner/test-output", test_suite)
    executor.COUNT += 1
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def channel_consume(channel, queue):
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def start():
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
        print("Running locally \nURL:" + amqp_url + "\nqueue: " + queue)

    connection = pika.BlockingConnection(url)
    channel = connect_to_receiving_channel(connection, queue)
    channel_consume(channel, queue)


start()
