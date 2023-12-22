from decouple import config
from redis import Redis
import logging

def get_redis_connection(db_select: int):
    redis_host = config('REDIS_CACHE_HOST')
    redis_port = config('REDIS_CACHE_PORT')
    redis_con = Redis(host=redis_host, port=redis_port, db=db_select)

    try:
        if not redis_con.ping():
            return None
    except Exception as e:
        logging.error(f'레디스 연결 오류: {e}')
        return None

    return redis_con
