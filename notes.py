"""
---  # repo_config.yaml
# model name: repo instance arguments
core.models.User:
  repo_class: RedisRepository
  db_name: redis
  foo: bar  
---  # db_config.yaml
# db backend name: db engine arguments
redis:
  host: localhost
  port: 6789
  db: 1
"""

# results in:
repo = RedisRepository(User, engine_config={'host': 'localhost', 'port': 6789, 'db': 1})

# --- dharma/domain/repos/redis.py

from dharma.compat.db import redis_engine


class RedisRepository(BaseRepository):

    def __init__(self, klass, engine_config):
        if not redis_engine:
            raise ConfigError
        super(RedisRepository, self).__init__(klass) 
        self.engine = redis_engine(**engine_config)


# --- dharma/compatibilities/db.py

try:
    from redis import StrictRedis as redis_engine
except ImportError:
    redis_engine = None


# --- requirements for tests

fakeredis==0.7.0

# --- requirements for py2.6

importlib==1.0.3
