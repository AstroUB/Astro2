# Will Edit them soon

import logging
import os
from pyrogram import filters
from pyrogram.types import Message
from startup.client import astro, assistant
from startup.config import HNDLR, PVT_GRP


class Logme:
    def __init__(self, message):
        self.chat_id = PVT_GRP
        self.message = message

    async def log_msg(self, client, text: str = "?"):
        if len(text) > 1024:
            try:
                file = await client.send_document(self.chat_id, make_file(text))
            except BaseException as e: 
                logging.error(str(e))
                return None
            os.remove('logger.log')
            return file
        else:
             try:
                 return await client.send_message(self.chat_id, text)
             except:
                 logging.error(str(e))
                 return None

    async def fwd_msg_to_log_chat(self):
        try:
            return await self.message.forward(self.chat_id)
        except BaseException as e: 
            logging.error(str(e))
            return None

def make_file(text):
    open("logger.log", "w").write(text)
    return "logger.log"

__all__ = (
  "astro",
  "HNDLR",
  "assistant",
  "filters",
  "Message",
  "Logme"
)
