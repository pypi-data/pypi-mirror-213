# rabbitmq_integration/__init__.py
from .rabbitmq_commands import Command as RabbitMQCommand

def register_commands():
    return {'rabbitmq': RabbitMQCommand()}
