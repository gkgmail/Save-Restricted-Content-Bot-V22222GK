# devggn
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

API_ID = int(getenv("API_ID", "28837789"))
API_HASH = getenv("API_HASH", "33c9162294cdd6c9d51d964e4469fadb")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = list(map(int, getenv("OWNER_ID", "8087702564").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://smallcapitaltrader1:XVsdQj8vu38ZIFoy@cluster0.9g3ri.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
LOG_GROUP=getenv("LOG_GROUP","https://t.me/+ekMWunqcukg0OTBl")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002445805057"))
