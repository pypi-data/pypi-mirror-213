import pika
import threading
import time

from simplerabbit.rabbit_base import RabBase


class RabbitReceiver(RabBase):
    def __init__(self, host='localhost', port='5672', username=None, password=None, virtual_host='/', ca_cert='', client_cert='', client_key=''):
        super().__init__(host, port, username, password, virtual_host, ca_cert, client_cert, client_key)
        self.on_message = None
        self.on_connection_closed = None
        self.is_consuming = False
        self.consumer_tag = None
        self.stop_event = threading.Event()
        self.consumer_thread = None
        self.queues = []

    def subscribe(self, queue_name, exchange, routing_key):
        print(f'Subcribe to exchange : {exchange} with routing key : {routing_key}')
        self.queues.append(queue_name)
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.queue_bind(exchange=exchange, queue=queue_name, routing_key=routing_key)

    def set_message_callback(self, on_message):
        self.on_message = on_message

    def set_connection_close_callback(self, cb):
        self.on_connection_closed = cb

    def start_consuming(self):
        self.is_consuming = True
        # Start consuming messages from the queue in a separate thread
        self.consumer_thread = threading.Thread(target=self._consume_messages)
        self.consumer_thread.start()

    def _consume_messages(self):
        for queue in self.queues:
            self.channel.basic_consume(queue=queue, on_message_callback=self._callback, auto_ack=True)
        print("Waiting for messages...")
        while not self.stop_event.is_set():
            try:
                self.channel.connection.process_data_events()
                time.sleep(0.2)
            except Exception as e:
                if self.on_connection_closed:
                    self.on_connection_closed()

    def _callback(self, ch, method, properties, body):
        if self.on_message:
            self.on_message(int(properties.correlation_id), body)

    def close(self):
        self.stop_consuming()
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except pika.exceptions.ConnectionWrongStateError as e:
                pass

    def stop_consuming(self):
        if self.channel:
            self.stop_event.set()  # Signal the consuming thread to stop
            try:
                self.channel.stop_consuming()
                self.channel.close()
                self.channel = None
            except Exception as e:
                pass



