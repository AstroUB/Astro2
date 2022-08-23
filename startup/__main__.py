from startup.client import astro, assistant
from pyrogram.errors import AccessTokenInvalid, ApiIdInvalid, ApiIdPublishedFlood
from startup.config import VC
import time
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [AstroUB] - %(levelname)s - %(message)s",
)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("apscheduler").setLevel(logging.ERROR)
INFO = logging.getLogger(__name__)


if __name__ == "__main__":
    try:
        assistant.start()  # Not using run as wanna print 
        print("•×•Assistant Started•×•")
        astro.run()
        INFO.info("ASTRO 2.0 is Started!!!!\n\nEnjoy🥳🥳")
        INFO.info("Please Join @Astro_UserBot for Updates Channel!")
        INFO.info("Join @Astro_HelpChat for Support Chat!")
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your TOKEN is not valid.")

# SOON Creating VC Client as well!
