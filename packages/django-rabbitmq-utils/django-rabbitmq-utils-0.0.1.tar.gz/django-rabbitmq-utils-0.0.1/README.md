# django_rabbitmq_utils

To enhance the RabbitMQ library features in Python Django, to utilize additional libraries and features that complement RabbitMQ's functionality.

## requirements

For running this, you need to have `python3` installed on your system.


## Installation
```
pip install django-rabbitmq-utils==0.0.1

```
## Example
<!-- Implemented retry mechanisms to improve the reliability of message processing in Django      application -->

```
from django_rabbitmq_utils.rabbitmq import send_message_with_retry, consume_messages_from_queue

def send_notification(message):
    send_message_with_retry(message)

def start_message_consumer():
    consume_messages_from_queue('my_queue')

```
<!-- Message routing patterns  in Django application -->

```
# settings.py
CELERY_QUEUES = getattr(settings, 'CELERY_QUEUES', ())
CELERY_QUEUES += message_routing.routing.get_queues()


# celery.py
from kombu import Connection
from django_rabbitmq_utils.routing import get_exchange

app = Celery('your_project')

@app.task(bind=True)
def process_message(self, body):
    # Connect to RabbitMQ and publish the message with routing key
    with Connection(app.broker_connection()) as connection:
        exchange = get_exchange()
        producer = connection.Producer(serializer='json')
        producer.publish(body, exchange=exchange, routing_key='key1')
```

<!-- Enhance the security of your RabbitMQ setup by configuring SSL/TLS encryption -->

```
# settings.py
import ssl
from django_rabbitmq_utils.rabbitmq_ssl import RABBITMQ_SSL_CONFIG

BROKER_URL = 'amqp://<username>:<password>@<rabbitmq_host>:<rabbitmq_port>/<vhost>'
BROKER_USE_SSL = True
BROKER_SSL_OPTIONS = RABBITMQ_SSL_CONFIG

```
<!-- Integrate RabbitMQ interfaces into  Django application -->

```
# seetings.py
COMMANDS = {
    **rabbitmq_integration.register_commands()
}

```