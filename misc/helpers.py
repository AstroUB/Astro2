import asyncio
import math
import os
from pyrogram.types import Message
from startup.config import SUDO
async def edit_or_reply(msg: Message, text, parse_mode="md"):
    if not msg:
        return await msg.edit(text, parse_mode=parse_mode)
    if not msg.from_user:
        return await msg.edit(text, parse_mode=parse_mode)
    if msg.from_user.id in SUDO:
        if msg.reply_to_message:
            kk = msg.reply_to_message.message_id
            return await msg.reply_text(
                text, reply_to_message_id=kk, parse_mode=parse_mode
            )
        return await msg.reply_text(text, parse_mode=parse_mode)
    return await msg.edit(text, parse_mode=parse_mode)
