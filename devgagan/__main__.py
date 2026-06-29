from flask import Flask, request
import telebot

TOKEN = "8005476267:AAFBCe2Vgr9MUdEk2iGsglMNaarYX83rR-U"
APP_URL = "https://app.koyeb.com/services/0f41edfe-bd2e-4c1a-bc3b-8cd6bdb58cdb"

# आपकी असली Dump ID यहाँ सेट है
DUMP_CHAT_ID = -1004447354945

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 1. /start कमांड के लिए
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Webhook connected 🚀")

# 2. डंप फीचर का मुख्य लॉजिक (यूज़र का हर बैच/फ़ाइल डंप में फॉरवर्ड होगा)
@bot.message_handler(func=lambda message: True, content_types=['text', 'audio', 'document', 'photo', 'video', 'voice'])
def handle_all_messages(msg):
    # यूज़र को रिप्लाई देना कि काम शुरू हो गया है
    bot.reply_to(msg, "Processing your request... 🔄")
    
    # डंप चैनल में फॉरवर्ड करने का सटीक कोड (बिना किसी फालतू शर्त के)
    try:
        # पहले डंप चैनल में यूज़र की जानकारी भेजें
        user_info = f"📥 **NEW BATCH REQUEST**\n\n👤 **Name:** {msg.from_user.first_name}\n🆔 **ID:** `{msg.from_user.id}`"
        bot.send_message(chat_id=DUMP_CHAT_ID, text=user_info)
        
        # अब यूज़र का भेजा हुआ मैसेज/फ़ाइल डंप चैनल में सीधे फॉरवर्ड करें
        bot.forward_message(
            chat_id=DUMP_CHAT_ID,
            from_chat_id=msg.chat.id,
            message_id=msg.message_id
        )
    except Exception as e:
        print(f"🔴 Dump Error: {e}")

# 3. Webhook Handling
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
