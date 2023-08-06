import pika
import sys
import json

START_CONSUMING = 'Waiting for messages. To exit press CTRL+C'


class BaseMqWorker:
    def __init__(self, mq_username, mq_password, mq_host, mq_port, mq_virtual_host, consume_queue, produce_queue, blocked_connection_timeout=None) -> None:
        self.__connection = None
        self.__channel = None
        self._mq_username = mq_username
        self._mq_password = mq_password
        self._mq_host = mq_host
        self._mq_port = mq_port
        self._mq_virtual_host = mq_virtual_host
        self._consume_queue = consume_queue
        self._produce_queue = produce_queue
        self._blocked_connection_timeout = blocked_connection_timeout

        pass

    def start_consuming(self, message: str = START_CONSUMING):
        print(message, file=sys.stderr)
        self.__channel.start_consuming()

    def __callback(self, ch, method, props, body):
        message = body.decode()
        self.consume(message)
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f'\n\r{START_CONSUMING}', file=sys.stderr)

    def consume(self, message):
        print(f'Recevied "{message}"', file=sys.stderr)
    
    def __enter__(self):
        credentials = pika.PlainCredentials(
            username=self._mq_username, password=self._mq_password)
        self.__connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self._mq_host, port=self._mq_port, credentials=credentials,
            heartbeat=0, virtual_host=self._mq_virtual_host, blocked_connection_timeout=self._blocked_connection_timeout)
        )

        self.__channel = self.__connection.channel()
        self.__channel.queue_declare(queue=self._consume_queue, durable=True)

        self.__channel.basic_qos(prefetch_count=1)
        self.__channel.basic_consume(
            queue=self._consume_queue, on_message_callback=self.__callback)

        return self

    
    def publish(self, message, queue=None, persistent=True):
        queue = queue or self._produce_queue

        self.__channel.basic_publish(exchange='',
                              routing_key=queue,
                              body=json.dumps(message),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE, ) if persistent else None)
        print (f'Published "{message}" to {queue}')

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def close_connection(self):
        self.__channel.stop_consuming()
        self.__connection.close()