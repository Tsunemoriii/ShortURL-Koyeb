import asyncio
import datetime
import io
import os
import random
import re
import string
import subprocess
import sys
import time
import traceback

import aiofiles
from pyrogram import filters
from pyrogram.errors import (
    FloodWait,
    InputUserDeactivated,
    ListenerCanceled,
    PeerIdInvalid,
    UserIsBlocked,
)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import C5 as cli
from bot.plugins import help_text_5 as help_text, start_text_5 as start_text
from bot.utils.config import (
    AUTH_USERS,
    SHORTENER_API_5 as SHORTENER_API,
    SHORTENER_WEB_5 as SHORTENER_WEB,
)
from bot.utils.database import db
from bot.utils.logger import Logger
from bot.utils.tools import (
    Base64,
    aexec,
    check_url,
    check_user,
    forcesub,
    make_short_url,
    shorten_url,
)

bot_id = 5
Files = []
broadcast_ids = {}


@cli.on_message(filters.private)
async def _(cli, cmd):
    await check_user(cli, cmd, bot_id)


@cli.on_message(
    filters.user(AUTH_USERS) & filters.private & filters.command("broadcast")
)
async def broadcast_handler_open(_, m):
    if m.reply_to_message is None:
        await m.delete()
    else:
        await broadcast(m, db)


@cli.on_message(filters.user(AUTH_USERS) & filters.private & filters.command("del"))
async def broadcast_handler_close(_, m):
    _list = m.text.split(" ", 1)
    if len(_list) == 1:
        await m.reply_text("Please give me the broadcast id.")
        return
    x = await m.reply_text("Deleting broadcasts...")
    broadcast_id = _list[1].strip()
    info = await db.get_broadcast_info(broadcast_id, bot_id)
    if info is None:
        await x.edit_text("Invalid/expired broadcast id.")
        return
    count = 0
    for i in info["msg_ids"]:
        await cli.delete_messages(int(i[1]), int(i[0]))
        count += 1
    await db.del_broadcast_info(broadcast_id, bot_id)
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    await x.edit_text(f"Deleted {count} messages.")


async def send_msg(user_id, message, broadcast_id):
    forward = await db.get_forward(bot_id)
    try:
        if forward is False:
            _id = await message.forward(chat_id=user_id)
        elif forward is True:
            _id = await message.copy(chat_id=user_id)
        _list = [_id.message_id, _id.chat.id]
        broadcast_ids[broadcast_id]["msg_id"].append(_list)
        return 200, None
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return send_msg(user_id, message)
    except InputUserDeactivated:
        return 400, f"{user_id} -:- deactivated\n"
    except UserIsBlocked:
        return 400, f"{user_id} -:- blocked the bot\n"
    except PeerIdInvalid:
        return 400, f"{user_id} -:- user id invalid\n"
    except Exception:
        return 500, f"{user_id} -:- {traceback.format_exc()}\n"


async def broadcast(m, db):
    all_users = await db.get_all_users(bot_id)
    broadcast_msg = m.reply_to_message
    while True:
        broadcast_id = "".join([random.choice(string.ascii_letters) for i in range(7)])
        if not broadcast_ids.get(broadcast_id):
            break
    out = await m.reply_text(
        text=f"Starting broadcast with id: `{broadcast_id}` \n\nYou'll get the log file after it's finised."
    )
    start_time = time.time()
    total_users = await db.total_users_count(bot_id)
    done = 0
    failed = 0
    success = 0
    broadcast_ids[broadcast_id] = dict(
        total=total_users, current=done, failed=failed, success=success, msg_id=[]
    )
    async with aiofiles.open(
        f"broadcast_{broadcast_id}.txt", "w"
    ) as broadcast_log_file:
        async for user in all_users:
            sts, msg = await send_msg(
                user_id=int(user["id"]),
                message=broadcast_msg,
                broadcast_id=broadcast_id,
            )
            if msg is not None:
                await broadcast_log_file.write(msg)
            if sts == 200:
                success += 1
            else:
                failed += 1
            if sts == 400:
                await db.delete_user(user["id"], bot_id)
            done += 1
            if broadcast_ids.get(broadcast_id) is None:
                break
            else:
                broadcast_ids[broadcast_id].update(
                    dict(current=done, failed=failed, success=success)
                )
    info = broadcast_ids[broadcast_id]["msg_id"]
    await db.set_broadcast_info(broadcast_id, info, bot_id)
    if broadcast_ids.get(broadcast_id):
        broadcast_ids.pop(broadcast_id)
    completed_in = datetime.timedelta(seconds=int(time.time() - start_time))
    await asyncio.sleep(3)
    await out.delete()
    if failed == 0:
        await m.reply_text(
            text=f"`{broadcast_id}`\nBroadcast completed successfully! \n\nTotal users: {total_users} \nTotal done: {done} \nTotal success: {success} \nTotal failed: {failed} \nCompleted in: {completed_in}",
            quote=True,
        )
    else:
        await m.reply_document(
            document=f"broadcast_{broadcast_id}.txt",
            caption=f"`{broadcast_id}`\nBroadcast completed successfully! \n\nTotal users: {total_users} \nTotal done: {done} \nTotal success: {success} \nTotal failed: {failed} \nCompleted in: {completed_in}",
            quote=True,
        )
    os.remove(f"broadcast_{broadcast_id}.txt")


@cli.on_message(filters.command("help") & filters.private)
async def help(_, m):
    buttons = [[InlineKeyboardButton("Close", callback_data="close")]]

    await m.reply_text(help_text, reply_markup=InlineKeyboardMarkup(buttons))


@cli.on_message(filters.command("start") & filters.private)
async def start(_, m):
    api = {
        "key": SHORTENER_API,
        "url": SHORTENER_WEB,
    }
    buttons = [[InlineKeyboardButton("Help", callback_data="help")]]
    # send link to user
    if len(m.command) > 1:
        try:
            _url = Base64.decode(m.command[1])
            await forcesub(cli, m, bot_id, _url)
            await make_short_url(m, api, _url)
            return
        except Exception as e:
            Logger.info(e)
            return
    else:
        await forcesub(cli, m, bot_id)
        try:
            await m.reply_text(
                start_text.format(mention=m.from_user.mention),
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        except Exception as e:
            Logger.info(f"[Exception in Start]: {e}")


@cli.on_message(filters.user(AUTH_USERS) & filters.private & filters.command("stats"))
async def sts(_, m):
    await m.reply_text(
        text=f"**Total users in Database:** `{await db.total_users_count(bot_id)}`",
        quote=True,
    )


@cli.on_message(filters.user(AUTH_USERS) & filters.command("settings"))
async def opensettings(_, m):
    await m.reply_text(
        f"**Here you can set broadcast settings:**",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        f"Tag Forward: {'OFF' if await db.get_forward(bot_id) else 'ON'}",
                        callback_data="forwardon",
                    )
                ],
                [InlineKeyboardButton("Close", callback_data="close")],
            ]
        ),
    )


@cli.on_message(
    filters.user(AUTH_USERS)
    & filters.command("short")
    & filters.private
    & filters.incoming
)
async def create(_, m):
    api = {
        "key": SHORTENER_API,
        "url": SHORTENER_WEB,
    }
    Files.append(m.from_user.id)
    btn = InlineKeyboardMarkup(
        [[InlineKeyboardButton("Cancel", callback_data="cancel")]]
    )
    try:
        long_url = await cli.ask(
            chat_id=m.from_user.id,
            text="Send me the url you want to shorten. Press cancel to exit.",
            reply_markup=btn,
            filters=filters.text,
        )
    except ListenerCanceled:
        return await m.reply_text("Cancelled!")
    except Exception as e:
        Logger.exception(e)
        return await m.reply_text(
            "Something went wrong! Try again later or contact @ForGo10God."
        )

    # generate short url
    message = await m.reply_text("Making short url...")
    if not SHORTENER_API:
        return await message.edit_text("No shortener api found!")
    if not check_url(long_url.text):
        return await message.edit_text("Invalid url type!")
    short_url = shorten_url(api, long_url.text)

    # generate bot start link
    base64_string = Base64.encode((long_url.text).strip())
    bot = await cli.get_me()
    bot_url = f"https://t.me/{bot.username}?start={base64_string}"

    # send link to user
    send_btn = [
        [InlineKeyboardButton("Short Url", url=short_url)],
        [InlineKeyboardButton("Bot Link", url=bot_url)],
        [InlineKeyboardButton("Original Url", url=long_url.text)],
    ]
    await message.edit_text(
        text="Your link has been generated successfully! Find them below.",
        reply_markup=InlineKeyboardMarkup(send_btn),
    )


@cli.on_message(filters.command("eval") & filters.user(AUTH_USERS))
async def eval_(_, message):
    status_message = await message.reply_text("Processing ...")
    cmd = message.text.split(" ", maxsplit=1)[1]
    reply_to_ = message
    if message.reply_to_message:
        reply_to_ = message.reply_to_message
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, cli, message)
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
        evaluation = "Success"
    final_output = "<b>EVAL</b>: "
    final_output += f"<code>{cmd}</code>\n\n"
    final_output += "<b>OUTPUT</b>:\n"
    final_output += f"<code>{evaluation.strip()}</code> \n"
    if len(final_output) > 4096:
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "eval.txt"
            await reply_to_.reply_document(
                document=out_file, caption=cmd[:1000], disable_notification=True
            )
    else:
        await reply_to_.reply_text(final_output)
    await status_message.delete()


@cli.on_message(filters.user(AUTH_USERS) & filters.command("term"))
async def terminal(_, message):
    if len(message.text.split()) == 1:
        await message.reply_text("Usage: `/term echo owo`")
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await message.reply_text(
                    """
**Error:**
```{}```
""".format(
                        err
                    ),
                    parse_mode="markdown",
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await message.reply_text(
                """**Error:**\n```{}```""".format("".join(errors)),
                parse_mode="markdown",
            )
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            filename = "output.txt"
            with open(filename, "w+") as file:
                file.write(output)
            await cli.send_document(
                message.chat.id,
                filename,
                reply_to_message_id=message.message_id,
                caption="`Output file`",
            )
            os.remove(filename)
            return
        await message.reply_text(f"**Output:**\n```{output}```", parse_mode="markdown")
    else:
        await message.reply_text("**Output:**\n`No Output`")
