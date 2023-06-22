from pyrogram import filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot import C4 as cli
from bot.plugins import help_text_4 as help_text, start_text_4 as start_text
from bot.plugins.plugin_4 import Files
from bot.utils.config import (
    SHORTENER_API_4 as SHORTENER_API,
    SHORTENER_WEB_4 as SHORTENER_WEB,
)
from bot.utils.database import db
from bot.utils.tools import chan, make_short_url

bot_id = 4


@cli.on_callback_query(filters.regex("^help$"))
async def help_cb(_, m):
    await m.answer()

    buttons = [
        [InlineKeyboardButton("Home", callback_data="home")],
        [InlineKeyboardButton("Close", callback_data="close")],
    ]

    await m.message.edit(text=help_text, reply_markup=InlineKeyboardMarkup(buttons))


@cli.on_callback_query(filters.regex("^close$"))
async def close_cb(_, m):
    try:
        await m.message.delete()
        await m.message.reply_to_message.delete()
    except:
        pass


@cli.on_callback_query(filters.regex("^home$"))
async def home_cb(_, m):
    await m.answer()

    buttons = [
        [InlineKeyboardButton("Help", callback_data="help")],
        [InlineKeyboardButton("Close", callback_data="close")],
    ]

    await m.message.edit(
        text=start_text.format(mention=m.from_user.mention),
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@cli.on_callback_query(filters.regex("^cancel$"))
async def done_cb(_, m):
    Files.remove(m.from_user.id)
    cli.cancel_listener(m.from_user.id)
    await m.message.delete()


@cli.on_callback_query(filters.regex("^forwardon$"))
async def callback_handlers(_, m):
    forward = await db.get_forward(bot_id)
    if forward is True:
        await db.set_forward("False", bot_id)
    else:
        await db.set_forward("True", bot_id)
    await m.message.edit(
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
    await m.answer(
        f"Successfully setted tag forward to: {'OFF' if await db.get_forward(bot_id) else 'ON'}"
    )


@cli.on_callback_query(filters.regex(r"retry#(.*)$"))
async def retry_cb(_, m):
    api = {
        "key": SHORTENER_API,
        "url": SHORTENER_WEB,
    }
    _list = m.data.split("#")
    _url = _list[1]
    channel = chan[bot_id - 1]
    ch_info = await cli.get_chat(channel)
    ch_title = ch_info.title
    ch_id = ch_info.id
    try:
        await cli.get_chat_member(ch_id, m.from_user.id)
    except UserNotParticipant:
        await m.answer(
            f"Join {ch_title} to use this bot.",
            show_alert=True,
        )
        return
    except:
        await m.answer("Something went wrong. Please try again later.", show_alert=True)
        return
    await make_short_url(m.message, api, _url, edit=True)
