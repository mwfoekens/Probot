import pika


def open_sending_connection(host: str) -> pika.BlockingConnection:
    """
    Open connection
    :param host:    Host name
    :return:        A connection
    """
    return pika.BlockingConnection(pika.ConnectionParameters(host=host))


def open_sending_channel(queue: str, connection: pika.BlockingConnection) -> pika.adapters.BlockingConnection.channel:
    """
    Open channel
    :param queue:       Name of the queue
    :param connection:  connection
    :return:        Return the channel
    """
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    return channel


def send_message(message: str, channel: pika.adapters.BlockingConnection.channel, queue: str) -> None:
    """
    Send message
    :param message: the message that will be sent
    :param channel: the channel that is used to publish
    :param queue:   name of the queue
    :return:        None
    """
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
            content_type="application/json"
        ))
    print("\tSent %r" % message)


def close_connection(connection: pika.BlockingConnection) -> None:
    """
    Close connection
    :param connection:  the connection that needs to be closed
    :return:            None
    """
    connection.close()
