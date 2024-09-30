import redis


# Redis details
REDIS_HOST = 'redis-db'
REDIS_PORT = 6379


# Redis connection
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

