from . import * 
from startup.config import PVT_GRP


@astro.on_message(filters.command("join", HNDLR))
async def join(astro: astro, e: Message):
    chat = e.text[6:]
    if chat.isnumeric():
        return await e.edit("Can't join a chat with chat id. Give username or invite link.")
    try:
      await astro.join_chat(chat)
      await e.edit("**Join Successfully ✅ **")
    except Exception as ex:
        await e.edit(f"**ERROR:** \n\n{str(ex)}")
    if PVT_GRP:
         try:
             await astro.send_message(PVT_GRP, f"Joined New Chat \n\n Chat: {chat} \n JOINED BY: {e.from_user.id}")
         except Exception as a:
             print(a)
             pass


@astro.on_message(filters.command("leave", HNDLR))
async def leave(astro: astro, e: Message):
    Kaal = ("".join(e.text.split(maxsplit=1)[1:])).split(" ", 1)
    if len(e.text) > 7:
        chat = Kaal[0]
        try:
           await astro.leave_chat(chat)
           await e.edit("**Left Successfully ✅ **")
        except Exception as ex:
           await e.edit(f"**ERROR:** \n\n{str(ex)}")
    else:
        chat = e.chat.id
        ok = e.from_user.id
        if int(chat) == int(ok):
            return await e.edit(f"Usage: {HNDLR}leave <chat username or id> or {HNDLR}leave (type in Group for Direct leave)")
        if int(chat) == -1001359155814:
              return e.edit("**Error**")
        try:
           await astro.leave_chat(chat)
           await e.edit("**Left Successfully ✅ **")
        except Exception as ex:
           await e.edit(f"**ERROR:** \n\n{str(ex)}")
        if PVT_GRP:
           try:
                await astro.send_message(PVT_GRP, f"Leaved Chat \n\n Chat: {chat} \n LEFT BY: {e.from_user.id}")
           except Exception as a:
             print(a)
             pass
