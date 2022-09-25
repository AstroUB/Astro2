from . import *
from startup.config import PVT_GRP

@astro.on_message(filters.command("gcast", HNDLR))
async def broadcast(_, e: Message):
    ok = e.from_user.id
    txt = ' '.join(e.command[1:])
    if txt:
      msg = str(txt)
    elif e.reply_to_message:
        msg = e.reply_to_message.text.markdown
    else:
        await e.edit("Give Message for Broadcast or reply to any msg")
        return

    await e.edit("__Broadcasting__")
    err = 0
    dn = 0

    async for cht in astro.get_dialogs():
          try:
                await astro.send_message(cht.chat.id, msg, disable_web_page_preview=True)
                dn += 1
                await asyncio.sleep(0.5)
          except Exception as e:
              err += 1 
    return await astro.send_message(ok, f"**• Broadcast Done** ✅ \n\n Chats: {dn} \n Failed In {err} chats")
    if PVT_GRP:
       try:
           await astro.send_message(PVT_GRP, f"Broadcasting Done By user {e.from_user.id} \n\n Chat: {dn} \n Failed in {err} chats")
       except Exception as a:
             print(a)
             await astro.send_message(PVT_GRP, f"GOT ERROR↓↓↓\n{a}")
