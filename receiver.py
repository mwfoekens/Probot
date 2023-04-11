import pika
import time
import json
import data_preparer


def open_receiving_connection(host):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host))


def connect_to_receiving_channel(connection, queue):
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    return channel


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body.decode())
    data = json.loads(body.decode())
    executor.generate_testsuite(data)
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def channel_consume(channel, queue):
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()


def start(queue, host):
    connection = open_receiving_connection(host)
    channel = connect_to_receiving_channel(connection, queue)
    channel_consume(channel, queue)


start("probot_queue", "localhost")
