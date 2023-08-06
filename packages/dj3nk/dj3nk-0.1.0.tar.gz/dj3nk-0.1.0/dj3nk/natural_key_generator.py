# -*- coding: utf-8 -*-
import random
from django.conf import settings

from a3redis.structures import String
from a3redis.bases import RedisClientFactory


DEFAULT_SETTINGS = {
    "increment_main_key": "a3:dj:nk",
    "random_bit_length": 16,
    "puzzle_count": 1000000,
    "rdb_conf_name": "default"
}


class NaturalKeyGenerator(object):

    def __init__(self, config: dict = None):
        config = config or getattr(settings, 'NATURAL_KEY', None) or DEFAULT_SETTINGS

        self._increment_main_key = config['increment_main_key']
        self._random_bit_length = config['random_bit_length']
        self._puzzle_count = config['puzzle_count']
        self._rdb_conf_name = config['rdb_conf_name']

        # python的int与sql bigint 都是64位，1位为符号位，最大值为9223372036854775807
        self._increment_bit_length = 63 - self._random_bit_length
        # stop_value - 1 == max_value
        self._stop_random_value = 1 << self._random_bit_length

    def get_core_increment_string(self) -> String:
        return String(main_key=self._increment_main_key, rdb=RedisClientFactory.get_rdb(name=self._rdb_conf_name))

    def puzzle(self, count: int = None) -> int:
        # 混淆
        if count is None:
            count = self._puzzle_count

        detail = random.randrange(count, count * 10)
        increment_string = self.get_core_increment_string()
        return increment_string.increase(detail)

    def generate_nk(self) -> int:
        # 默认自增位为47,最大值为140737488355328，按100年需求来算，每天可用近40亿
        increment = self.get_core_increment_string().increase()
        random_value = random.randrange(0, self._stop_random_value)
        return increment << self._random_bit_length | random_value
