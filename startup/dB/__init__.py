import os
import logging
import os
import time
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from startup.config import MONGO_DB

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [AstroUB] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)

mongodb = MongoClient(MONGO_DB)


try:
    mongo_client.server_info()
except ConnectionFailure:
    logging.error("Invalid Mongo DB URL. Please Check Your Credentials! Astro2.0 is Exiting!")
    quit(1)



dtbs = mongodb["Astro"]