import secrets
import time

import pika
from pika.exceptions import AMQPConnectionError

from src.base.client.constants import CLIENT_STOPPED
from src.base.client.messages.serializer import Serializer
from src.base.client.messages.message import Message
from src.base.logging.log_handler import LogWarning
from src.base.states.event import Event
from src.base.states.handler import Handler


class Client:

    def __init__(self, id: str, message_broker: str, port: int, handler: Handler):
        self.queue_name = None
        self.listening_connection = None
        self.listening_channel = None
        self.id = id
        self.serializer = Serializer()
        self.hostname = message_broker
        self.exchange_name = "swarm_learning"
        self.handler = handler
        self.stop = False

    def get_connection(self):
        return pika.BlockingConnection(pika.ConnectionParameters(self.hostname))

    def get_channel(self):
        return self.get_connection().channel()

    def join(self):
        self.stop = False
        while not self.stop:
            try:
                self.listening_channel = self.get_channel()
                self.listening_channel.exchange_declare(exchange=self.exchange_name, exchange_type='fanout')
                result = self.listening_channel.queue_declare(queue='', exclusive=True)
                self.queue_name = result.method.queue
                self.listening_channel.queue_bind(exchange=self.exchange_name, queue=self.queue_name)
                self.listening_channel.basic_consume(queue=self.queue_name,
                                                     auto_ack=True,
                                                     on_message_callback=self.handle_on_message)
                self.listening_channel.start_consuming()
            except AMQPConnectionError:
                self.handler.queue_event(LogWarning("client.join", extra={
                    "hostname": self.hostname,
                    "error": "connection"
                }))
                time.sleep(2)
        self.handler.queue_event(Event(CLIENT_STOPPED))

    def quit(self):
        self.stop = True
        self.listening_channel.stop_consuming()

    def handle_on_message(self, ch, method, properties, body):
        message = self.serializer.deserialize(body)
        if message.from_id != self.id:
            self.handler.queue_event(message)

    def send(self, message: Message):
        tries = 3
        while tries > 0:
            try:
                serialized_message = self.serializer.serialize(message)
                channel = self.get_channel()
                channel.basic_publish(exchange=self.exchange_name, routing_key='', body=serialized_message)
                tries = 0
            except AMQPConnectionError:
                self.handler.queue_event(LogWarning("client.send", extra={
                    "hostname": self.hostname,
                    "error": "connection"
                }))
                time.sleep(2)
            finally:
                tries -= 1