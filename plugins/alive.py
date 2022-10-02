# All copyRights are reserved! 
# https://DevAdarsh.me/
# https://github.com/AstroUB/Astro2.0


from . import *
import os
import sys
import asyncio
import datetime
import time
from plugins import vision, python
from startup.config import ALV_PIC, ALV_TXT

async def get_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    hmm = len(time_list)
    for x in range(hmm):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "
    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time


@astro.on_message(filters.command("alive", HNDLR))
async def zindahu(astro, msg: Message):
    user = await msg.from_user.mention
    start = datetime.datetime.now()
    uptime = await get_time((time.time() - start_time))
    text = f"""

        {ALV_TXT}
    Astro-Vision: `{vision}`
    Python-Vision: `{python}`
    uptime: `{uptime}`
    DATABASE: `MongoDB`
    Support: [HELPCHAT](https://t.me/Astro_helpchat)
    Updates: [CHANNEL](https://t.me/Astro_Userbot)

    My Master: [{user}]
    """
    if ALV_PIC:
        if ALV_PIC.endswith(".jpg", ".png", ".jpeg"):
            await astro.send_photo(msg.chat.id, ALV_PIC, caption=text)
        if ALV_PIC.endswith(".mp4", ".gif"):
            await astro.send_video(msg.chat.id, ALV_PIC, caption=text)
    else: 
        await astro.send_message(msg.chat.id, text)
