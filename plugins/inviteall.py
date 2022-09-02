

from . import *

def get_params(text):
    return [ t for t in text.split() if t.startswith('-') ]

@astro.on_message(filters.command("invite", HNDLR))
async def ins(astro, message: Message):
    params  = get_params(message.text)
    invite_String = "**Invited** - %s**"
    txt = message.text
    chet = message.chat.id
    if "-all" in params:
        async for member in astro.iter_chat_members(txt.split()[2]):
            user = member.user.id
            c = 0
            a = 0
            try:

                await astro.add_chat_members(chet, user)
                a += 1
            except Exception:
                c += 1
            await message.edit(invite_String % (a) + f"\n**Failed** - {c}")
    else:
        chet = message.chat.id
        usr: str  = txt.split()[1]
        user = (await astro.get_users(
            int(usr) if usr.isalnum() else usr
        ))
        try:
            await astro.add_chat_members(chet, user.id)
            await message.edit(invite_String % (user.mention(style="md")))

        except BaseException as e:
            await message.edit(f"**ERROR** - `{e}`")
