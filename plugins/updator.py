
# All rights reserved.

from startup.config import HEROKU_API_KEY, HEROKU_APP_NAME, PVT_GRP

from pyrogram import filters
from pyrogram.types import Message
from os import environ, execle, path, remove
from git import Repo
from datetime import datetime
import heroku3
import asyncio
import sys
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from . import *


REPO = "https://github.com/AstroUB/Astro2.0"
U_BRANCH = "main"

def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    heroku_applications = heroku.apps()
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace(
            "https://", "https://api:" + api_key + "@"
        )

HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)

requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)
async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)

def gen_change_Log(repo, diff):
    ch_log = ""
    for c in repo.iter_commits(diff):
        ch_log += f"🔨 **#{c.count()} :** [{c.summary}]({REPO}/commit/{c}) 👷 __{c.author}__ \n"
    return ch_log


@astro.on_message(filters.command("update", HNDLR) & filters.me)
async def update_it(client, msg: Message):
    msg_ = await msg.edit("Searching for Update🔍🔍")
    repo = REPO
    ac_br = repo.active_branch.name
    changelog = await gen_change_Log(repo, f"HEAD..upstream/{ac_br}")
    if not changelog:
        await msg.edit("**Your Astro is already** __Updated__\n\n🌿**B R A N C H: [[{ac_br}]]({REPO}/tree/{ac_br})** ")
    else: 
        changelog_str = (
            f"**🛰️New UPDATE AVALIABLE🤩**\n\n🌿B R A N C H: [[{ac_br}]]({REPO}/tree/{ac_br}):\n\n"
            + "**CHANGELOG📃📰**\n\n"
            + f"{changelog}"
            + "\n\n\nUse `updateme` to updates your bot"
        )
        if len(changelog_str) > 4096:
            await msg.edit("`Changelog is too big, view the file to see it.`")
            file = open("Changes.txt", "w+")
            file.write(changelog_str)
            file.close()
            await astro.send_document(
                msg.chat.id,
                "Changes.txt",
            )
            remove("Changes.txt")
        else:
            await msg.edit(changelog_str)
            return

@astro.on_message(filters.command("updateme", HNDLR) & filters.me)
async def updating(_, msg: Message):  
    # A Fact: who gets more Horny after watching porn? 
    # Ans: Girls  
    try:
        repo = Repo()
        ac_br = repo.active_branch.name
    except InvalidGitRepositoryError:
        repo = Repo.init()
    if "upstream" in repo.remotes:
        origin = repo.remote("upstream")
    else:
        origin = repo.create_remote("upstream", REPO)
    origin.fetch()
    repo.create_head(U_BRANCH, origin.refs.main)
    repo.heads.main.set_tracking_branch(origin.refs.main)
    repo.heads.main.checkout(True)
    if repo.active_branch.name != U_BRANCH:
        await msg.edit(f"`Seems Like You Are Using Custom Branch - {ac_br}! Please Switch To {U_BRANCH} To Make This Updater Function!`")
        return
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(U_BRANCH)
    if not HEROKU_URL:
        try:
            ups_rem.pull(U_BRANCH)
        except GitCommandError:
            repo.git.reset('--hard', 'FETCH_HEAD')
        await updateme_requirements()
        await msg.edit("`Updated Sucessfully! Give Me A min To Restart!`")
        args = [sys.executable, "-m", "startup"]
        execle(sys.executable, *args, environ)
        return
    else:
        await msg.edit("Heroku Detected! Pushing, Please Wait..5min\nCheck your bot")
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(HEROKU_URL)
        else:
            remote = repo.create_remote("heroku", HEROKU_URL)
        try:
            remote.push(refspec="HEAD:refs/heads/main", force=True)
            await astro.send_message(PVT_GRP, "Master!\nAstro2.0 is Updated Successfully!\nIf you will face Any Issue in Future Please let my Developer(s) to know it😇 at\n→ @Astro_HelpChat\n\n~Enjoy🥰✨")
        except BaseException as error:
            return await msg.edit(f"**Updater Error** \nTraceBack : `{error}`")
        await msg.edit("`Build Started! Please Wait For 10-15 Minutes!`")
