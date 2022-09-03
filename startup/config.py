import os

VC = os.environ.get("VC" "OFF")
SUDO_ID = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
SUDO = list(SUDO_ID)
HNDLR = os.environ.get("HNDLR", ".")
DEV = set(int(x) for x in os.environ.get("DEV", "").split())
MANAGER = os.environ.get("MANAGER", "OFF")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")
MONGO_DB = os.environ.get("MONGO_DB", "")
TIMEZONE = os.environ.get("TIMEZONE", "")
ALV_PIC = os.environ.get("ALV_PIC", '')
ALV_TEXT = os.environ.get("ALV_TEXT", "")




PVT_GRP = os.environ.get("PVT_GRP", None)
if PVT_GRP is not None:
        try:
            PVT_GRP = int(PVT_GRP)
        except ValueError:
            raise ValueError(
                "Invalid Private Group ID. Make sure your ID is starts with -100 and make sure that it is only numbers.")

