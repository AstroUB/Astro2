import asyncio
import sys 
import subprocess 
from pyrogram import filters
from pyrogram.types import Message
from startup.config import SUDO_ID, HNDLR

from . import *

async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


@astro.on_message(filters.command("bash", HNDLR) & filters.me)
async def bash_run(_, msg: Message):
      await msg.edit("__Processing...__")
      try:
        cmd = msg.text.split(" ", maxsplit=1)[1]
      except IndexError:
        return await msg.edit("Invalid Syntax")
      stdout, stderr = await bash(cmd)
      OUT = f"**•⋗ Bᴀsʜ\n\n• COMMAND:**\n`{cmd}` \n\n"
      if stderr:
        OUT += f"**• Eʀʀᴏʀ:** \n`{stderr}`\n\n"
      if stdout:
        _o = stdout.split("\n")
        o = "\n".join(_o)
        OUT += f"**• OUTPUT:**\n`{o}`"
      if not stderr and not stdout:
        OUT += "**• OUTPUT:**\n`Success`"
      await msg.edit(OUT)
      if msg.from_user.id in DEV: # If from user id
         await msg.reply(OUT)
      if msg.from_user.id in SUDO_ID:
         await msg.reply("`Dev user required...`")