# coding=utf-8
import unittest
from halring.rabbitmq_lib.halring_rabbitmq import Publisher
from halring.rabbitmq_lib.halring_rabbitmq import MQClient
import time
import random


class TestRabbitmqUtilPublisher(unittest.TestCase):

    def test_001_publisher(self):
        mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")
        connection = mqclient.connect()
        queue = "test_queue"

        print(mqclient.is_connect())

        a = Publisher(connection)
        # a.send_message(message ={"delivery_task_id":"1617", "MQ_total":2, "module_id_set":[1],
        # "module_id_set_total":[1,2,3]},queue=queue)
        # time.sleep(10)
        a.send_message(message={"delivery_task_id": "1617", "module_set": ["auto_deploy"]}, queue=queue)
        # a.send_message(message ={"delivery_task_id":"1617", "MQ_total":2, "module_id_set":[2,3]},queue=queue)
        # a.send_message(message ={"delivery_task_id":"3333", "MQ_total":3, "publish_time":"", "randomint":0},
        # queue=queue)

        connection.close()

    def test_002_timer_publisher(self):
        mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")

        queue = "test_queue"
        while True:
            x = random.randint(0, 100)
            print(str(x))
            if x > 1:
                connection = mqclient.connect()
                print(mqclient.is_connect())
                a = Publisher(connection)
                t = time.localtime()
                t_str = time.strftime("%Y%m%d%H%M%S", t)
                a.send_message(message={"publish_time": t_str, "randomint": str(x)}, queue=queue)
                connection.close()
                print(mqclient.is_connect())
                break
            time.sleep(600)
