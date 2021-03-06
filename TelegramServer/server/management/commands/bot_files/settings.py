import telebot
import os
from TelegramServer.settings import BASE_DIR

with open(os.path.join(BASE_DIR, 'token.txt'), 'r') as token:
    TOKEN = token.read()

bot = telebot.TeleBot(TOKEN)
