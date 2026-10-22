# ---------------------------------------------------
# File Name: __init__.py
# Description: A Pyrogram bot for downloading files from Telegram channels or groups 
#              and uploading them back to Telegram.
# Author: Gagan
# GitHub: https://github.com/devgaganin/
# Telegram: https://t.me/team_spy_pro
# YouTube: https://youtube.com/@dev_gagan
# Created: 2025-01-11
# Last Modified: 2025-01-11
# Version: 2.0.5
# License: MIT License
# ---------------------------------------------------
# FIX: Bot ab BINA session string ke chalega.
# STRING / DEFAULT_SESSION khaali ho, galat ho ya duplicate ho —
# bot CRASH NAHI hoga. Users apna /login khud karenge (phone + OTP).
# Telethon start fail (FloodWait) par bhi bot chalta rahega.

import asyncio
import logging
import time
from pyrogram import Client
from pyrogram.enums import ParseMode 
from config import API_ID, API_HASH, BOT_TOKEN, STRING, MONGO_DB, DEFAULT_SESSION
from telethon.sync import TelegramClient
from motor.motor_asyncio import AsyncIOMotorClient

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s",
    level=logging.INFO,
)

botStartTime = time.time()

app = Client(
    "pyrobot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    workers=100,
    parse_mode=ParseMode.MARKDOWN
)


def _start_telethon(session_name):
    """Telethon client start karo. Fail ho jaye (FloodWait etc.) to
    bot crash nahi hoga — sirf Telethon wale features (YTDL) rukenge,
    main bot normal chalega."""
    client = TelegramClient(session_name, API_ID, API_HASH)
    try:
        return client.start(bot_token=BOT_TOKEN)
    except Exception as e:
        print(f"Telethon {session_name} start fail: {e} - bot phir bhi chalega", flush=True)
        try:
            client.disconnect()
        except Exception:
            pass
        return client


sex = _start_telethon('sexrepo')

if STRING:
    pro = Client("ggbot", api_id=API_ID, api_hash=API_HASH, session_string=STRING, workers=100)
else:
    pro = None


if DEFAULT_SESSION:
    userrbot = Client("userrbot", api_id=API_ID, api_hash=API_HASH, session_string=DEFAULT_SESSION, workers=100)
else:
    userrbot = None

telethon_client = _start_telethon('telethon_session')

# MongoDB setup
tclient = AsyncIOMotorClient(MONGO_DB)
tdb = tclient["telegram_bot"]  # Your database
token = tdb["tokens"]

async def create_ttl_index():
    """Ensure the TTL index exists for the `tokens` collection."""
    await token.create_index("expires_at", expireAfterSeconds=0)

# Run the TTL index creation when the bot starts
async def setup_database():
    await create_ttl_index()
    print("MongoDB TTL index created.")

async def restrict_bot():
    global BOT_ID, BOT_NAME, BOT_USERNAME, pro, userrbot
    await setup_database()
    await app.start()
    getme = await app.get_me()
    BOT_ID = getme.id
    BOT_USERNAME = getme.username
    BOT_NAME = f"{getme.first_name} {getme.last_name}" if getme.last_name else getme.first_name
    
    # Session-string wale clients OPTIONAL hain — start fail ho jaye
    # (duplicate/dead string) to bot NAHI rukega, sirf wo client band hoga.
    if pro:
        try:
            await pro.start()
            print("STRING userbot start ho gaya", flush=True)
        except Exception as e:
            print(f"STRING session start fail ({e}) - ignore karke bot chalega. Users apna /login karenge.", flush=True)
            pro = None
    if userrbot:
        try:
            await userrbot.start()
            print("DEFAULT_SESSION userbot start ho gaya", flush=True)
        except Exception as e:
            print(f"DEFAULT_SESSION start fail ({e}) - ignore karke bot chalega.", flush=True)
            userrbot = None

loop.run_until_complete(restrict_bot())
