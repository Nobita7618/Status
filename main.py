import os
import asyncio
import datetime
import pytz

from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.errors import FloodWait

load_dotenv()

app = Client(name="UserBot",
             api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"),
             session_string=os.getenv("SESSION_STRING"))

bot = Client(name="Bot",
             api_id=int(os.getenv("API_ID")),
             api_hash=os.getenv("API_HASH"),
             bot_token=os.getenv("BOT_TOKEN"))

BOT_LIST = [x.strip() for x in os.getenv("BOT_LIST").split(' ')]
CHANNEL_OR_GROUP_ID = int(os.getenv("CHANNEL_OR_GROUP_ID"))
MESSAGE_ID = int(os.getenv("MESSAGE_ID"))
TIME_ZONE = os.getenv("TIME_ZONE")

OWNER_ID = None
if id:=os.getenv("OWNER_ID"):
    OWNER_ID = int(id)

bot.start()


async def main():
    print("Status Checker Bot Started")
    async with app:
        while True:
            TEXT = "✨ **ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ғᴀʟʟᴇɴ ᴀssᴏᴄɪᴀᴛɪᴏɴ ʙᴏᴛ's sᴛᴀᴛᴜs ᴄʜᴀɴɴᴇʟ**\n\n❄ ʜᴇʀᴇ ɪs ᴛʜᴇ ʟɪsᴛ ᴏғ ᴛʜᴇ ʙᴏᴛ's ᴡʜɪᴄʜ ᴡᴇ ᴏᴡɴ ᴀɴᴅ ᴛʜᴇɪʀ sᴛᴀᴛᴜs (ᴀʟɪᴠᴇ ᴏʀ ᴅᴇᴀᴅ), ᴛʜɪs ᴍᴇssᴀɢᴇ ᴡɪʟʟ ᴋᴇᴇᴘ ᴜᴘᴅᴀᴛɪɴɢ ᴏɴ **ᴇᴠᴇʀʏ 10-15 ᴍɪɴᴜᴛᴇs.**"
            for bots in BOT_LIST:
                ok = await app.get_users(f"@{bots}")
                try:
                    await app.send_message(bots, "/statusbot")
                    await asyncio.sleep(2)
                    messages = app.get_chat_history(bots, limit=1)
                    async for x in messages:
                        msg = x.text
                    if msg == "/statusbot":
                        TEXT += f"\n\n🤖 - **[{ok.first_name}](tg://openmessage?user_id={ok.id}): ❌ ᴏғғʟɪɴᴇ**"
                        if OWNER_ID:
                            await bot.send_message(OWNER_ID, f'Alert {ok.first_name} is ᴏғғʟɪɴᴇ 💀')
                    else:
                        TEXT += f"\n\n🤖 - **[{ok.first_name}](tg://openmessage?user_id={ok.id}): ✅ ᴏɴʟɪɴᴇ**\n**{msg}**"
                    await app.read_chat_history(bots)
                except FloodWait as e:
                    await asyncio.sleep(e.value)
            time = datetime.datetime.now(pytz.timezone(f"{TIME_ZONE}"))
            date = time.strftime("%d %b %Y")
            time = time.strftime("%I:%M: %p")
            TEXT += f"\n\nʟᴀsᴛ ᴄʜᴇᴄᴋᴇᴅ ᴏɴ : \nᴅᴀᴛᴇ : {date}\nᴛɪᴍᴇ : {time}"
            await bot.edit_message_text(int(CHANNEL_OR_GROUP_ID), MESSAGE_ID,
                                        TEXT)
            await asyncio.sleep(900)


bot.run(main())
