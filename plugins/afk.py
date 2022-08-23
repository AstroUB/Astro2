

from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime
import asyncio
from . import *
from misc import *

from startup.db.afkdb import (
    no_afk,
    go_afk,
    check_afk
)



@astro.on(filters.command("afk", HNDLR) & filters.me)
async def set_afk(_, message: Message):
    name = message.from_user.mention
    pablo = await edit_or_reply(message, "__Processing...__")
    msge = None
    msge = get_text(message)
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    log = Logme(message)
    if msge:
        msg = f"**{name}** \n__Going Afk Because Of😴💤__ `{msge}`"
        await log.log_msg(client, f"#AfkLogger\n\nMaster your AFK is Activated✅\nR E A S O N: `{msge}`",)
        go_afk(afk_start, msge)
    else:
        msg = f"**I am very Busy Right Now🥵🥵\nI can't talk to your now!!😅\n\nPlease Wait until i will come back😁**."
        await log.log_msg(client, f"#AfkLogger Afk Is Active",)
        go_afk(afk_start) 
    await pablo.edit(msg)
        
@dynamic(filters.mentioned & ~filters.me & ~filters.bot & ~filters.edited & filters.incoming)
async def afk_er(client, message):
    lol = check_afk()
    if not lol:
        message.continue_propagation()
    reason = lol["reason"]
    if reason == "":
        reason = None
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    afk_since = "**a while ago**"
    message_to_reply = (f"I Am **[AFK]** Right Now. \n**Last Seen :** `{total_afk_time}`\n**Reason** : `{reason}`" if reason else f"I Am **[AFK]** Right Now. \n**Last Seen :** `{total_afk_time}`")
    LL = await message.reply(message_to_reply)
    await asyncio.sleep(8)
    await LL.delete()
    message.continue_propagation()
        
@dynamic(filters.outgoing & filters.me)
async def no_afke(client, message):
    lol = check_afk()
    if not lol:
        message.continue_propagation()
    back_alivee = datetime.now()
    afk_start = lol["time"]
    afk_end = back_alivee.replace(microsecond=0)
    total_afk_time = str((afk_end - afk_start))
    kk = await message.reply(f"""__Pro is Back Alive__\n**No Longer afk.**\n `I Was afk for:``{total_afk_time}`""",)
    await kk.delete()
    no_afk()
    log = Logme(message)
    await log.log_msg(client, f"#AfkLogger User is Back Alive ! No Longer Afk\n AFK for : {total_afk_time} ")
    message.continue_propagation()