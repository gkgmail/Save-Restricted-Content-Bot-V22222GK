from flask import Flask, request
import telebot

TOKEN = "8005476267:AAFBCe2Vgr9MUdEk2iGsglMNaarYX83rR-U"
APP_URL = "https://app.koyeb.com/services/0f41edfe-bd2e-4c1a-bc3b-8cd6bdb58cdb"

# ⚠️ यहाँ -100xxxxxxxxx को हटाकर अपने Dump Group या Channel की ID डालें
DUMP_CHAT_ID = -100xxxxxxxxx  

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# 1. /start कमांड के लिए
@bot.message_handler(commands=['start'])
def start(msg):
    bot.reply_to(msg, "Webhook connected 🚀")

# 2. डंप फीचर का मुख्य लॉजिक (यह यूज़र की हर फ़ाइल/बैच को डंप में भेजेगा)
@bot.message_handler(func=lambda message: True, content_types=['text', 'audio', 'document', 'photo', 'video', 'voice'])
def handle_all_messages(msg):
    # (यहाँ आपका बैच निकालने या फाइल डाउनलोड/अपलोड करने का कोड काम करेगा)
    # उदाहरण के लिए हम यूज़र को एक रिप्लाई भेज रहे हैं:
    sent_msg = bot.reply_to(msg, "Processing your request... 🔄")
    
    # डंप चैनल में भेजने का कोड
    if DUMP_CHAT_ID != -100xxxxxxxxx:
        try:
            # bot.copy_message यूज़र द्वारा भेजी गई फ़ाइल को बिना दोबारा अपलोड किए सीधे डंप में कॉपी कर देगा
            bot.copy_message(
                chat_id=DUMP_CHAT_ID,
                from_chat_id=msg.chat.id,
                message_id=msg.message_id,
                caption=f"👤 **User:** {msg.from_user.first_name}\n🆔 **ID:** `{msg.from_user.id}`\n🌐 **Username:** @{msg.from_user.username if msg.from_user.username else 'None'}"
            )
        except Exception as e:
            print(f"Dump Group में भेजने में एरर आया: {e}")

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

# Webhook सेट करना
bot.remove_webhook()
bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
