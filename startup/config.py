import os

VC = os.environ.get("VC" "OFF")
SUDO_ID = set(int(x) for x in os.environ.get("SUDO_USERS", "").split())
HNDLR = os.environ.get("HNDLR", ".")
DEV = set(int(x) for x in os.environ.get("DEV", "").split())
MANAGER = os.environ.get("MANAGER", "OFF")
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", "")
HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", "")
