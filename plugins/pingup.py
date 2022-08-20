# Astro2.0 
# (c) All CopyRights are reserved by Team of Astro2.0
# https://github.com/AstroUB.Astro2.0
# Please Give Credits while doing Foke / Kang 


import time
from datetime import datetime 
from pyrogram import filters
from pyrogram.types import Message
from startup.config import SUDO_ID
from . import * 



@astro.on_message(filters.command("ping", HNDLR) & filters.me)
async def ping(_, msg: Message):
    mention = msg.from_user.mention
    start = datetime.now()
    event = await msg.edit("•🅟🅞🅝🅖•")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    textt = """
★°:･✧*.°☆.*★°●¸★　 
▃▃▃▃▃▃▃▃▃▃▃
┊ ┊ ┊ ┊ ┊ ┊┊
┊ ┊ ┊ ┊ ˚✩ ⋆｡˚ ✩
┊ ┊ ┊ ┊⍣∙°⚝○｡°✯
┊ ┊ ┊ ┊
┊ ┊ ┊ ⛦『P‌๏‌и‌ɠ‌』 
┊ ┊ ┊︎✫ ˚♡ ⋆˚ ⋆｡ ❀
┊ ┊ ┊
┊ ┊ ┊𓆩𝙈𝙎--≻{} ﮩ٨ـﮩﮩ٨ـ𓆪
┊ ┊ ✯
┊ ✬ ˚•˚✩
┊⍣ •°
┊亗•ʍʏ ๏ωиэя•亗
★• {} •
⚘ ƛsτʀ๏ υsєяъ๏т ⚘
""".format(ms, mention)
    await msg.edit(textt)
    if msg.from_user.id in SUDO_ID:
        await msg.reply(textt)
