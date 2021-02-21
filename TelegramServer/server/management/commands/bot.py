from django.core.management.base import BaseCommand, CommandError
import telebot

TOKEN = "1664099561:AAHWc4tQ2Lckr2XwZy7fJqyAKyclj5ysuy4"
bot = telebot.TeleBot(TOKEN)

class Command(BaseCommand):
    help = 'Запусти бота'

    @bot.message_handler(commands=['start', 'help'])
    def start(message: telebot.types.Message):
        text = f"{message.chat.username}, я могу подсказать текущий курс валют! \n\n" \
               f"Для этого введите: \n<имя валюты> <в какую валюты перевести>" \
               f"<количество переводимой валюты> \n\nНапример, евро доллар 100 \n\n" \
               f"Чтобы увидеть список доступных валют: /values"
        bot.send_message(message.chat.id, text)

    def handle(self, *args, **options):
        print('start bot')
        bot.polling(none_stop=True)

