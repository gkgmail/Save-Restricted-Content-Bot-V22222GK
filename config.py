# devgagan - fixed config (env missing ho to crash nahi hoga)

from os import getenv

INST_COOKIES = """
# write up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""


def _int_env(name, default=0):
    try:
        return int(getenv(name, "") or default)
    except (TypeError, ValueError):
        return default


API_ID = _int_env("API_ID")
API_HASH = getenv("API_HASH", "")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = [int(x) for x in getenv("OWNER_ID", "").split() if x.lstrip("-").isdigit()]
MONGO_DB = getenv("MONGO_DB", "")
LOG_GROUP = getenv("LOG_GROUP", "")
CHANNEL_ID = _int_env("CHANNEL_ID")
FREEMIUM_LIMIT = _int_env("FREEMIUM_LIMIT", 0)
PREMIUM_LIMIT = _int_env("PREMIUM_LIMIT", 500)
WEBSITE_URL = getenv("WEBSITE_URL", "upshrink.com")
AD_API = getenv("AD_API", "52b4a2cf4687d81e7d3f8f2b7bc2943f618e78cb")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAULT_SESSION", None)
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
