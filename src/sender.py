import pika
import click
import json


def send_messages(host: str, port: int, queue: str, groups: list):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)

    click.secho("Connected. Sending: ", fg='cyan')
    for item in groups:
        message = json.dumps(item)
        channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=message,
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE,
                content_type="application/json"
            ))
        print("\tSent %r" % message)

    connection.close()
