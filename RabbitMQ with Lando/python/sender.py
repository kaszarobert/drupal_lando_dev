import pika
import time

def send_message():
    credentials = pika.PlainCredentials('admin', 'admin')
    parameters = pika.ConnectionParameters(
        host='rabbitmq_rabbitmq_1',        # vagy 'rabbitmq' ha docker-compose service
        port=5672,
        virtual_host='/',
        credentials=credentials
    )

    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
 
    channel.queue_declare(queue='hello', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body='Hello World!',
        properties=pika.BasicProperties(
            delivery_mode=2,  # 2 = persistent
        )
    )
    print(" [x] Sent 'Hello World!'")

    connection.close()

if __name__ == "__main__":
   send_message()