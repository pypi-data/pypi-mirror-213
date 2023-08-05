# coding=utf-8
import unittest
from redis_lib.halring_redis import RedisUtil


class TestRedisUtil(unittest.TestCase):

    def test_redis_publish(self):
        input_ip = "127.0.0.1"
        input_user = "root"
        input_pwd = "root"
        input_db = "test"
        rds_cli = RedisUtil()
        # redis连接
        rds_cli.redis_connect(input_ip, input_user, input_pwd, input_db)
        rds_cli.redis_publish('channel', 'msg')

    def test_redis_subscribe(self):
        input_ip = "127.0.0.1"
        input_user = "root"
        input_pwd = "root"
        input_db = "test"
        rds_cli = RedisUtil()
        # redis连接
        rds_cli.redis_connect(input_ip, input_user, input_pwd, input_db)
        rds_cli.redis_subscribe('channel')

