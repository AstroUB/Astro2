from startup.client import astro, assistant
from pyrogram.errors import AccessTokenInvalid, ApiIdInvalid, ApiIdPublishedFlood
from startup.config import VC



if __name__ == "__main__":
    try:
        assistant.start()  # Not using run as wanna print 
        print("•×•Assistant Started•×•")
        astro.run()
        print("ASTRO 2.0 is Started!!!!\n\nEnjoy")
        print("Please Join @Astro_UserBot for Updates Channel!")
        print("Join @Astro_HelpChat for Support Chat!")
    except (ApiIdInvalid, ApiIdPublishedFlood):
        raise Exception("Your API_ID/API_HASH is not valid.")
    except AccessTokenInvalid:
        raise Exception("Your TOKEN is not valid.")

# SOON Creating VC Client as well!