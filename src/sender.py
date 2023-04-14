import pika


def open_sending_connection(host):
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host))


def open_sending_channel(queue, host):
    connection = open_sending_connection(host)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    return channel


def send_message(message, channel, queue):
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            content_type="application/json"
        ))
    print(" [x] Sent %r" % message)


def close_connection(connection):
    connection.close()
