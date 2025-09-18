import os

import pika


def send_message_to_rabbitmq(queue_name, message_body):
    """
    Establishes a connection to RabbitMQ, sends a message to a queue, and closes the connection.
    """

    rabbitmq_url = os.getenv(
        "RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

    try:
        connection = pika.BlockingConnection(pika.URLParameters(rabbitmq_url))
        channel = connection.channel()

        channel.queue_declare(queue=queue_name)

        channel.basic_publish(
            exchange="", routing_key=queue_name, body=message_body)

        print(f" [x] Sent '{message_body}' to queue '{queue_name}'")

        connection.close()
    except pika.exceptions.AMQPConnectionError as e:
        print(f"Failed to connect to RabbitMQ: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
