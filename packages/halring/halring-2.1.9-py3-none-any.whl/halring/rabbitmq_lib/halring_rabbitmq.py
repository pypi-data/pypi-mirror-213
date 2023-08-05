# -*- coding:utf-8 -*-
import pika
import json
from loguru import logger


class MQClient(object):
    def __init__(self, host, user, password, virtual_host, port=5672):
        """
        :param host: rabbitMQ服务地址
        :param user: rabbitMQ用户
        :param password: rabbitMQ密码
        :param virtual_host: rabbitMQ对应的虚拟主机，aqc使用的为aqc
        :param port: rabbitMQ端口，默认5672
        """
        self._host = host
        self._virtual_host = virtual_host
        self._port = port
        self._credentials = pika.PlainCredentials(user, password)

        # LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
        #               '-35s %(lineno) -5d: %(message)s')

    def connect(self):
        """
        返回pika.BlockingConnection
        """

        # heartbeat=600
        # blocked_connection_timeout=300
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host, virtual_host=self._virtual_host, port=self._port,
                                      credentials=self._credentials, heartbeat=0))

        logger.info("Connect %s success" % self._host)
        return self._connection

    def is_connect(self):
        """
        :return: 如果connection存在则True反之False
        """
        return self._connection.is_open

    def close_connection(self):
        """
        关闭连接
        """
        self._connection.close()
        logger.info("close connection success")


class Consumer(object):
    """
    消费者
    """
    def __init__(self, connection):
        """
        :param connection: pika.BlockingConnection

        """
        self._connection = connection
        self._channel = connection.channel()

    def callback(self, channel, method, properties, body):
        """
        需自行重写callback内容
        """
        print(body.decode())
        # 已配置自动ack所以不用再调用basic_ack
        # channel.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self, queue):

        try:
            result = self._channel.basic_consume(queue, self.callback, auto_ack=True)
            # result2= self._channel.basic_consume(queue2, self.callback, auto_ack=True)

            logger.info("start consumer")
            self._channel.start_consuming()
        except KeyboardInterrupt:
            self._channel.stop_consuming()
            logger.info("stop consumer")

    def close_channel(self):
        """
        :return: 关闭信道channel
        """
        self._channel.close()


class Publisher(object):
    """
    生产者
    """
    def __init__(self, connection):
        """
        :param connection: pika.BlockingConnection

        """
        self._connection = connection
        self._channel = connection.channel()

    def send_message(self, message, queue, exchange="", durable=True, routing_key=""):
        """
        :param message: 消息内容
        :param queue: 发送队列
        :param exchange: 交换机，默认为空""
        :param durable: 队列是否为持久化的，默认为True
        :param routing_key: 路由关键字，默认为""
        :return: 发送成功/失败 True/False
        """
        result = self._channel.queue_declare(queue=queue, durable=durable)

        callback_queue = result.method.queue
        routing_key = queue if routing_key == "" else routing_key
        message_str = json.dumps(message)

        try:
            self._channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message_str, mandatory=True)
            return True
        except Exception as e:
            return False

    def get_channel(self):
        """
        :return: 返回信道channel
        """
        return self._channel

    def close_channel(self):
        """
        :return: 关闭信道channel
        """
        self._channel.close()


if __name__ == '__main__':
    # public
    mqclient = MQClient(host="10.112.15.114", user="aqc001", password="L@rtern@9c", virtual_host="aqc")
    connection = mqclient.connect()
    queue = "auto_deploy_test"
    mqclient.close_connection()


    # publisher

    # a=Publisher(connection)
    # a.send_message(message ={"test":"message"},queue=queue)
    # a.send_message(message ={"test":"test"},queue=queue)

    # consumer

    class MyConsumer(Consumer):
        def callback(self, channel, method, properties, body):
            message = body.decode()
            temp_message = json.loads(message)

            if temp_message.get("test") == "message":
                print(temp_message.get("test"))

                channel.basic_ack(delivery_tag=method.delivery_tag)


    consumer = MyConsumer(connection)
    consumer.start_consuming(queue)

    # mqclient.close_connection()
