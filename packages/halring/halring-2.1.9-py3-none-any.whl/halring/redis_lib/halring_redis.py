# -*- coding:utf-8 -*-
import json
import time
import redis
from loguru import logger


class RedisUtil(object):
    def __init__(self):
        self._redis_producer = None

    def redis_connect(self, host, port, pwd, db):
        self._redis_producer = redis.Redis(host, port, password=pwd, db=db, decode_responses=True)

    def redis_publish(self, channel, msg):
        # dumps 用于将python对象编码成 json
        self._redis_producer.publish(channel, json.dumps(msg))

    def redis_subscribe(self, channel):
        sc = self._redis_producer.pubsub()
        sc.subscribe(channel)
        sc.parse_response()
        return sc

    # 消息队列 发布
    def redis_send_list_msg(self, key, msg):
        try:
            self._redis_producer.lpush(key, msg)
            logger.info("redis cache set. Key={}, Msg={}, ", key, msg)
        except Exception as e:
            logger.error("redis cache put exception. Key={}, " + str(e), key)

    # 消息队列 订阅
    def redis_sub_scribe(self, key):
        # brpop 与 rpop的区别是 brpop 当前队列中无数据时会阻塞，不会继续轮询
        json_object = self._redis_producer.brpop(key)
        if json_object is not None:
            logger.info("任务id，key，message")
            return json_object

    def redis_send_json_msg(self, key, msg):
        try:
            self._redis_producer.lpush(key, json.dumps(msg))
            logger.info("redis cache set. Key={}, Msg={}", key, msg)
        except Exception as e:
            logger.error(str(e))

    def redis_send_msg(self, key, msg):
        try:
            self._redis_producer.set(key, msg)
        except Exception as e:
            logger.error(str(e))

    def redis_remove_list(self, key):
        try:
            self._redis_producer.ltrim(key)
            self._redis_producer.zadd()
        except Exception as e:
            logger.error(str(e))

    def redis_zset_pub(self, key, msg):
        try:
            zset_size = self._redis_producer.zcard(key)
            # 序列化
            # map_msg = {json.dumps(msg): zset_size + 1}
            # time作为score，用time排序
            map_msg = {json.dumps(msg): time.strftime("%Y%m%d%H%M%S", time.localtime())}
            zset_result = self._redis_producer.zadd(key, map_msg)
            if zset_result == 0:
                logger.error("插入数据重复，请检查数据内容")
            else:
                logger.info("插入数据成功, key={}, msg={}, time={}", key, map_msg, time.strftime("%Y%m%d%H%M%S", time.localtime()))
        except Exception as e:
            logger.error(str(e))

    def redis_zset_sub(self, key):
        try:
            size = self._redis_producer.zcard(key)
            if size == 0:
                # logger.info("key={}, 消息队列为空", key)
                return
            zset_element = self._redis_producer.zrange(key, 0, 0)
            # 反序列化
            zset_json = json.loads(zset_element[0])
            logger.info("key={}, msg={}", key, zset_json[0])
            return zset_json[0]
        except Exception as e:
            logger.error(str(e))

    def redis_zset_commit(self, key):
        try:
            size = self._redis_producer.zcard(key)
            if size == 0:
                # logger.info("key={}, 消息队列为空", key)
                return
            zset_element = self._redis_producer.zrange(key, 0, 0)
            # for i in range(0, size):
            remove_result = self._redis_producer.zrem(key, zset_element[0])
            if remove_result != 0:
                logger.info("数据消费完成: key={}, msg={}", key, zset_element[0])
            else:
                logger.error("清除数据异常，请检查数据是否存在")
            return True
        except Exception as e:
            logger.error(str(e))

    def redis_poll(self, timeout, key):
        try:
            json_list = []
            if timeout < 0:
                logger.error("参数不正确，timeout必须为正整数")
            start_time = time.strftime("%Y%m%d%H%M%S", time.localtime())
            remaining_time = timeout
            while remaining_time > 0:
                json_object = self.redis_sub_scribe(key)
                if json_object is not None:
                    json_list.append(json_object)
                elapsed = int(time.strftime("%Y%m%d%H%M%S", time.localtime())) - int(start_time)
                remaining_time = timeout - int(elapsed)
        except Exception as e:
            logger.error("数据拉取不正确" + str(e))
