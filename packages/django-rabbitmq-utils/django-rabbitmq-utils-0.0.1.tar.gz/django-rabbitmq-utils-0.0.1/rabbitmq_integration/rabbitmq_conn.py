import pika

def get_rabbitmq_connection():
    # Define your RabbitMQ connection parameters
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters('localhost', 5672, '/', credentials)

    # Establish the RabbitMQ connection
    connection = pika.BlockingConnection(parameters)
    return connection

def publish_message(queue_name, message):
    connection = get_rabbitmq_connection()
    channel = connection.channel()

    # Declare the queue
    channel.queue_declare(queue=queue_name)

    # Publish the message to the queue
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)

    # Close the connection
    connection.close()


# seetings.py
# COMMANDS = {
#     **rabbitmq_integration.register_commands()
# }