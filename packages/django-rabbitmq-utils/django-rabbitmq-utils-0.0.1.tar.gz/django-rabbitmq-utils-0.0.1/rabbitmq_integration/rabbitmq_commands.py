from django.core.management.base import BaseCommand
from .rabbitmq_api import RabbitMQAPI

class Command(BaseCommand):
    help = 'Fetches and displays RabbitMQ queues'

    def handle(self, *args, **options):
        # Initialize RabbitMQAPI with connection details
        rabbitmq_api = RabbitMQAPI("http://localhost:15672/api", "admin", "password")
        
        # Fetch queues using RabbitMQAPI
        queues = rabbitmq_api.get_queues()
        
        # Display queue details
        self.stdout.write("RabbitMQ Queues:")
        for queue in queues:
            self.stdout.write(f"Queue Name: {queue['name']}")
            self.stdout.write(f"Message Count: {queue['messages']}")
            self.stdout.write(f"Consumers: {queue['consumers']}")
            self.stdout.write('\n')
