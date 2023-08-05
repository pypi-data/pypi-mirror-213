# coding=utf-8
import unittest
import json
from halring.rabbitmq_lib.halring_rabbitmq import Consumer
from halring.rabbitmq_lib.halring_rabbitmq import MQClient


class TestRabbitmqUtilConsumer(unittest.TestCase):

    def test_001_consumer(self):

        mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")
        connection = mqclient.connect()
        queue = "test_queue"

        class MyConsumer(Consumer):
            def callback(self, channel, method, properties, body):
                message = body.decode()
                temp_message = json.loads(message)
                print(message)

        consumer = MyConsumer(connection)
        consumer.start_consuming(queue)


if __name__ == '__main__':
    a = TestRabbitmqUtilConsumer().test_001_consumer()
