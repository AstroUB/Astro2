from pyrogram import filters
from pyrogram.types import Message 

from . import *

@assistant.on_message(filters.command("/start"))
async def start(_, msg: Message):
   name = msg.from_user.mention
   await assistant.send_message(msg.chat.id, f"**HI**\n\nI am **A S T R O** assistant of {name}\n\nYou can contact to my master via me😉😊")
