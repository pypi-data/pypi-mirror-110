from typing import Optional, Dict, List
import uuid
import random

from redis import Redis

import rfq.redis


def publish(topic: str, message: Dict[str, str], front: bool, redis: Optional[Redis] = None) -> str:
    return publish_batch(topic=topic, messages=[message], front=front, redis=redis)[0]


def publish_batch(topic: str, messages: List[Dict[str, str]], front: bool, redis: Optional[Redis] = None) -> List[str]:
    r = rfq.redis.default() if redis is None else redis

    msgids = []

    if front:
        messages = list(reversed(messages))

    with r.pipeline() as tx:
        for message in messages:
            # https://github.com/python/cpython/blob/ba251c2ae6654bfc8abd9d886b219698ad34ac3c/Lib/uuid.py#L599-L612
            node = random.getrandbits(48) | (1 << 40)

            msgid = uuid.uuid1(node=node).hex

            msgids.append(msgid)

            tx.hset("rfq:{topic}:message:{msgid}".format(topic=topic, msgid=msgid), mapping=message)

            if front:
                tx.rpush("rfq:{topic}:backlog".format(topic=topic), msgid)
            else:
                tx.lpush("rfq:{topic}:backlog".format(topic=topic), msgid)

        tx.execute()

    return msgids
