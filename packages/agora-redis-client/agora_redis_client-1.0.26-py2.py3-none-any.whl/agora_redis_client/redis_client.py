from agora_config import config
from agora_logging import logger
import redis

class RedisClientSingleton(redis.Redis): 
    _instance: redis.Redis = None
    """
    Connects to the Redis Server from Agora Core    
    """
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self): 
        self.configure()
        super().__init__(host=self.server, port=self.port, decode_responses=True, socket_keepalive=True)        

    def configure(self):
        self.server = config["AEA2:RedisClient:Server"]
        if self.server == "":
            self.server = "localhost"

        self.port = config["AEA2:RedisClient:Port"]
        if self.port == "":
            self.port = "6379"

        logger.info("AEA2:RedisClient:")
        logger.info(f"--- Server: {self.server}")
        logger.info(f"--- Port: {self.port}")        
      
    def is_connected(self):
        try:             
            if self.ping():                
                return True
        except Exception as e:
            logger.error(
                f"Failed to connect to {self.server}:{self.port} :{str(e)}")
            return False

redis = RedisClientSingleton()
