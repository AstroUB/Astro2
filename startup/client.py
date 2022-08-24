import os
from pyrogram import Client

API_ID = int(os.environ.get("API_ID", 0))
API_HASH = os.environ.get("API_HASH", "")
SESSION = os.environ.get("SESSION", "")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")


astro = Client(
    name="[AstroUB]",
    session_string=SESSION,
    api_id=API_ID,
    api_hash=API_HASH,
    in_memory=True,
    plugins={'root': 'plugins'}
)

assistant = Client(
    "DynamicAdi",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins={'root': 'assistant'}
)
