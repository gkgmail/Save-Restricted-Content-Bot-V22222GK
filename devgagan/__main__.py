from flask import Flask, request
import telebot

TOKEN = "8005476267:AAFBCe2Vgr9MUdEk2iGsglMNaarYX83rR-U"
APP_URL = "https://app.koyeb.com/services/0f41edfe-bd2e-4c1a-bc3b-8cd6bdb58cdb"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Webhook connected 🚀")

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def home():
    return "Bot is alive"

bot.remove_webhook()
bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
