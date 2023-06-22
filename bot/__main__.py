import asyncio

from pyrogram import idle

from bot import ShortUrlBot
from bot.utils.logger import Logger


async def main():
    Logger.info("___ Starting The Bots ___")
    for i in ShortUrlBot:
        Logger.info(f">> Starting bot: {i.index + 1}")
        await i.start()
    Logger.info("___ Started The Bots ___")
    await idle()
    Logger.info("___ Stopping The Bots ___")
    for i in ShortUrlBot:
        Logger.info(f">> Stopping bot: {i.index + 1}")
        await i.stop()
    Logger.info("___ Stopped The Bots ___")

if __name__ == "__main__":
    for i,c in enumerate(ShortUrlBot):
        c.index = i
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
