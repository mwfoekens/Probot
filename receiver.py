import pika
import time


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
    time.sleep(body.count(b'.'))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def channel_consume(channel, queue):
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, on_message_callback=callback)

    channel.start_consuming()

# connection = open_receiving_connection()
# channel = connect_to_receiving_channel(connection)
# channel_consume(channel)
