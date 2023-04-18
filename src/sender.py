import pika


def open_sending_connection(host):
    """
    Open connection
    :param host:
    :return:
    """
    return pika.BlockingConnection(
        pika.ConnectionParameters(host=host))


def open_sending_channel(queue, host):
    """
    Open channel
    :param queue:
    :param host:
    :return:
    """
    connection = open_sending_connection(host)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    return channel


def send_message(message, channel, queue):
    """
    Send message
    :param message:
    :param channel:
    :param queue:
    :return:
    """
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
    """
    Close connection
    :param connection:
    :return:
    """
    connection.close()
