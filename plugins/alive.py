# All copyRights are reserved! 
# https://DevAdarsh.me/
# https://github.com/AstroUB/Astro2.0


from . import *
from plugins import vision, python
from startup.config import ALV_PIC, ALV_TXT


@astro.on_message(filters.command("alive", HNDLR))
async def zindahu(astro, msg: Message):
    user = await msg.from_user.mention
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