import sys
import io
import traceback

from pyrogram import filters
from pyrogram.types import Message 
from startup.config import SUDO_ID, DEV, HNDLR
from . import *


@astro.on_message(filters.command('eval', HNDLR) & filters.me)
async def cmdrunner(_, msg: Message):
    await msg.edit("Processing...")
    cmd = msg.text.split(" ", maxsplit=1)[1]
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, msg)
    except Exception:
        exc = traceback.format_exc()

    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr

    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success✅"

    final_output = "**EXEC**: `{}` \n\n **OUTPUT**: \n`{}` \n".format(cmd, evaluation)
    
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.text"
            await astro.send_file(
                msg.chat.id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=f"**PROCCESSED**: `{cmd[:1000]}`",
            )
            await astro.delete()
    else:
        await msg.edit(final_output)
    if msg.from_user.id in DEV:
        await msg.reply(final_output)
    if msg.from_user.id in SUDO_ID:
        await msg.reply("**DEV** `user is Required....`")


async def aexec(code, mesg: Message):
    exec(
        (f"async def __aexec(msg: Message): " + "\n msg = msg")
        + "\n chat = msg.chat.id"
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](msg)

