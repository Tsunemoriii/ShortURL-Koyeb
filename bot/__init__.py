from pyrogram import Client
from pyromod import listen

from bot.utils.config import (API_HASH, API_ID, BOT_TOKEN, BOT_TOKEN_2,
                              BOT_TOKEN_3, BOT_TOKEN_4, BOT_TOKEN_5)

ShortUrlBot = []

C1 = C2 = C3 = C4 = C5 = None

if BOT_TOKEN:
    C1 = Client(
        "ShortUrlBot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="bot.plugins"),
        workers=1000,
    )
    ShortUrlBot.append(C1)

if BOT_TOKEN_2:
    C2 = Client(
        "ShortUrlBot2",
        bot_token=BOT_TOKEN_2,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="bot.plugins"),
        workers=1000,
    )
    ShortUrlBot.append(C2)

if BOT_TOKEN_3:
    C3 = Client(
        "ShortUrlBot3",
        bot_token=BOT_TOKEN_3,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="bot.plugins"),
        workers=1000,
    )
    ShortUrlBot.append(C3)

if BOT_TOKEN_4:
    C4 = Client(
        "ShortUrlBot4",
        bot_token=BOT_TOKEN_4,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="bot.plugins"),
        workers=1000,
    )
    ShortUrlBot.append(C4)

if BOT_TOKEN_5:
    C5 = Client(
        "ShortUrlBot5",
        bot_token=BOT_TOKEN_5,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=dict(root="bot.plugins"),
        workers=1000,
    )
    ShortUrlBot.append(C5)
    
