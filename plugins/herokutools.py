
import asyncio
from functools import wraps
import time
import heroku3
from asyncio import sleep
from pyrogram.types import ChatPermissions
import os

from misc import *
from . import *

from startup.config import HEROKU_API_KEY, HEROKU_APP_NAME

heroku_client = None
if HEROKU_API_KEY:
    heroku_client = heroku3.from_key(HEROKU_API_KEY)
    
def _check_heroku(func):
    @wraps(func)
    async def heroku_cli(astro, message):
        heroku_app = None
        if not heroku_client:
            await edit_or_reply(message, "`Please Add Heroku API Key For This To Function To Work!`")
        elif not HEROKU_APP_NAME:
            await edit_or_reply(message, "`Please Add Heroku APP Name For This To Function To Work!`")
        if (HEROKU_APP_NAME and heroku_client):
          try:
            heroku_app = heroku_app(HEROKU_APP_NAME)
          except:
            await edit_or_reply(message, "`Heroku Api Key And App Name Doesn't Match!`")
          if heroku_app:
            await func(astro, message, heroku_app)
    return heroku_cli

@astro.on_message(filters.command("reboot", HNDLR) & filters.me)
@_check_heroku
async def gib_restart(astro, message, hap):
  msg_ = await edit_or_reply(message, "`[HEROKU] - 🔁 Restarting 🔁`")
  hap.restart()



@astro.on_message(filters.command("logs", HNDLR) & filters.me)
@_check_heroku
async def gib_logs(astro, message, happ):
  msg_ = await edit_or_reply(message, "__Please Wait!__")
  logs = happ.get_log()
  capt = f"Heroku Logs Of {HEROKU_APP_NAME}"
  await edit_or_send_as_file(logs, msg_, client, capt, "logs")


@astro.on_message(filters.command("setconfig", HNDLR) & filters.me)
@_check_heroku
async def set_varr(astro, message, app_):
  msg_ = await edit_or_reply(message, "__Please Wait!__")
  heroku_var = app_.config()
  _var = get_text(message)
  if not _var:
        await msg_.edit("`Here is Usage Syntax : .setconfig KEY|VALUE`")
        return
  if not '|' in _var:
        await msg_.edit("`Here is Usage Syntax : .setconfig KEY|VALUE`")
        return
  var_ = _var.split('|')
  if len(var_) > 2:
        await msg_.edit("`Here is Usage Syntax : .setconfig KEY|VALUE`")
        return
  _varname, _varvalue = var_
  await msg_.edit(f"`Variable {_varname} Added With Value {_varvalue}!`")
  heroku_var[_varname] = _varvalue


@astro.on_message(filters.command("delconfig", HNDLR) & filters.me)
@_check_heroku
async def del_varr(astro, message, app_):
  msg_ = await edit_or_reply(message, "`Please Wait!`")
  heroku_var = app_.config()
  _var = get_text(message)
  if not _var:
        await msg_.edit("`Give Var Name As Input!`")
        return
  if not _var in heroku_var:
        await msg_.edit("`This Var Doesn't Exists!`")
        return
  await msg_.edit(f"`Sucessfully Deleted {_var} Var!`")
  del heroku_var[_var]
