import os
class config:
    SECRET_KEY='12345698765409876'
    SQLALCHEMY_DATABASE_URI='sqlite:///mydb.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECURITY_PASSWORD_SALT='pass_salt_here'
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = 'redis://localhost:6379/1'
    CACHE_DEFAULT_TIMEOUT = 300