import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import logging
import requests
import telebot
from flask import Flask, request
import threading
#from ..config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Здесь я буду отправлять тебе уведомления о критических ошибках в 'technoblog'")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        return 'Content-Type not supported!'

def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    response = requests.post(url, json=payload)
    return response

def start_bot():
    bot.remove_webhook()
    bot.set_webhook(url='https://your-domain.com/webhook')
    app.run(host='0.0.0.0', port=5000)

