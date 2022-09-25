from datetime import datetime
from . import *



@astro.on_message(filters.command("stats", HNDLR))
async def stats(_, message: Message):
    await message.edit_text("Collecting stats")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh=await astro.get_me()
    group = ["supergroup", "group"]
    async for dialog in astro.iter_dialogs():
        if dialog.chat.type == "private":
            u += 1
        elif dialog.chat.type == "bot":
            b += 1
        elif dialog.chat.type == "group":
            g += 1
        elif dialog.chat.type == "supergroup":
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in ("creator", "administrator"):
                a_chat += 1
        elif dialog.chat.type == "channel":
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await message.edit_text(
        """`⚡️⚡️Your Stats Obtained in {} seconds⚡️⚡️`
__🤫You have {} Private Messages🤫.__
__✨ You are in {} Groups✨.__
__🔥You are in {} Super Groups🔥.__
__⭐️You Are in {} Channels⭐️.__
__🌟You Are Admin in {} Chats🌟.__
__❇️Bots = {}❇️__\n\n\n**S T A T S** Obtained by\n**A S T R O-UB**""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )
