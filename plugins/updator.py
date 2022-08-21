# All CopyRights are Reserved by Team of Astro2.0
# https://github.com/AstroUB/Astro2.0
# Keep the Credits While Foke / Kang

"""
Updater for Updating Future Changes in Astro2.0
"""
import heroku3
import asyncio
import sys
from os import environ, execle, path, remove

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import filters
from pyrogram.types import Message

from startup.config import HEROKU_APP_NAME, HEROKU_API_KEY

from . import *



requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


GIT_REPO_NAME = "Astro2.0"
UPSTREAM_REPO_URL = "https://github.com/AstroUB/Astro2.0"


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On " + "%d/%m/%y" + " at " + "%H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by **{c.author}**\n"
    return ch_log


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


@astro.on_message(filters.command("update", HNDLR) & filters.me)
async def upstream(_, ups: Message):
    "For .update command, check if the bot is up to date, update if specified"
    await ups.edit("__Searching🔍\nfor Update__")
    # conf = ups.pattern_match.group(1)
    off_repo = UPSTREAM_REPO_URL
    force_updateme = False

    # try:
    #     txt = "`Oops.. Updater cannot continue as "
    #     txt += "some problems occured`\n\n**LOGTRACE:**\n"
    repo = Repo()
    # except NoSuchPathError as error:
    #     await ups.edit(f"{txt}\n`directory {error} is not found`")
    #     repo.__del__()
    #     return
    # except GitCommandError as error:
    #     await ups.edit(f"{txt}\n`Early failure! {error}`")
    #     repo.__del__()
    #     return
    # except InvalidGitRepositoryError as error:
    #     await ups.edit(
    #             f"**Unfortunately, the directory {error} does not seem to be a git repository.\
    #             \nOr Maybe it just needs a sync verification with {GIT_REPO_NAME}\
    #         \nBut we can fix that by force updating the userbot using** `{HNDLR}update_astro`."
    #         )
        # return
        # repo = Repo.init()
        # origin = repo.create_remote("upstream", off_repo)
        # origin.fetch()
        # force_updateme = True
        # repo.create_head("main", origin.refs.main)
        # repo.heads.main.set_tracking_branch(origin.refs.main)
        # repo.heads.main.checkout(True)

    ac_br = repo.active_branch.name
    if ac_br != "main":
        await ups.edit(
            f"**[UPDATER]:**` Looks like you are using your own custom branch ({ac_br}). "
            "in that case, Updater is unable to identify "
            "which branch is to be merged. "
            "Please checkout the official branch of TeleBot`"
        )
        repo.__del__()
        return

    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass

    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)

    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")

    if not changelog and not force_updateme:
        await ups.edit(
            f"\nYour Astro2.0 **up-to-date**\n\nWith Branch🌿: **[[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})**\n\nRepo✨: [Astro2.0🛰️]({UPSTREAM_REPO_URL})\n"
        )
        repo.__del__()
        return

    if not force_updateme:
        changelog_str = (
            f"**🛰️New UPDATE AVALIABLE🤩**\n\n🌿B R A N C H: [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):\n\n"
            + "**CHANGELOG📃📰**\n\n"
            + f"{changelog}"
        )
        if len(changelog_str) > 4096:
            await ups.edit("`Changelog is too big, view the file to see it.`")
            file = open("Changes.txt", "w+")
            file.write(changelog_str)
            file.close()
            await ups.client.send_file(
                ups.chat_id,
                "Changes.txt",
                reply_to=ups.id,
            )
            remove("Changes.txt")
        else:
            await ups.edit(changelog_str)
        await ups.respond(f"Do {HNDLR}update_astro` to update🛰️")
        return

@astro.on_message(filters.command("update_astro", HNDLR) & filters.me)
async def updating(_, ups: Message):
    await ups.edit("Scanning new codes for Latest Update!")
    repo = Repo()
    # We're in a Heroku Dyno, handle it's memez.
    if HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await ups.edit(
                "__Please set up the__ `HEROKU_APP_NAME` __variable to be able to update astro__"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await ups.edit(
                f"{txt}\nInvalid Heroku credentials please correct them first!!"
            )
            repo.__del__()
            return
        await ups.edit(
            "Updating in progress, please wait for it to complete."
        )
        ups_rem = repo.remote("upstream")
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec="HEAD:refs/heads/main", force=True)
        except GitCommandError as error:
            await ups.edit(f"{txt}\n`Here is the error log:\n{error}`")
            repo.__del__()
            return
        await ups.edit("__Successfully Updated!__\n" "**Restarting**, `please wait...`")
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await ups.edit(
            "__Successfully Updated!__\n" "Bot is restarting...!\nWill Avaliable in few Seconds!🥰🍭"
        )
        # Spin a new instance of bot
        args = [sys.executable, "-m", "startup"]
        execle(sys.executable, *args, environ)
        return
