from django.core.management.base import BaseCommand, CommandError
from server.models import Payment, Score
import telebot
from telebot import types
from urllib.request import urlopen

# from .bot_files.extensions import text, text1


TOKEN = "1664099561:AAHWc4tQ2Lckr2XwZy7fJqyAKyclj5ysuy4"
bot = telebot.TeleBot(TOKEN)


class Command(BaseCommand):
    help = 'Запусти бота'

    def handle(self, *args, **options):
        print('starting telegram_bot')

        @bot.message_handler(commands=['start', 'help'])
        def start(message: telebot.types.Message):

            # Проверяем, есть ли запись счетов в базе данных
            if Score.objects.count() > 0:
                text = f"Добрый день {message.chat.username}.\nВведите сумму займа: \n\n"
                bot.reply_to(message, text)

                @bot.message_handler(content_types=['text'])
                def send_text(message):
                    if type(int(message.text)) == int:
                        text2 = f'Вы ввели сумму {int(message.text)}. Если это верно, то подтвердите:'
                        keyboard1 = types.InlineKeyboardMarkup()  # Готовим кнопки
                        key_yes = types.InlineKeyboardButton(text='Подтвердить', callback_data='yes')
                        key_no = types.InlineKeyboardButton(text='Ввести повторно', callback_data='no')
                        keyboard1.add(key_yes, key_no)  # И добавляем кнопку на экран
                        bot.send_message(message.from_user.id, text2, reply_markup=keyboard1)



            else:
                text1 = f"Добрый день {message.chat.username}.\nВыберите, что необходимо сделать: \n\n"
                keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
                key_report = types.InlineKeyboardButton(text='Получить график погашения',
                                                        callback_data='give_me_report')
                keyboard.add(key_report)  # И добавляем кнопку на экран
                bot.send_message(message.from_user.id, text1, reply_markup=keyboard)

        # Обработчик нажатия на кнопки
        @bot.callback_query_handler(func=lambda call: True)
        def calbak_worker(call):
            if call.data == 'give_me_report':
                page = urlopen('http://127.0.0.1:8000/')
                with open("График.html", "wb") as report:
                    report.write(page.read())
                    print('save')
                bot.send_document(call.message.chat.id, open(r'График.html', 'rb'))
            if call.data == 'yes':
                bot.send_message(call.message.chat.id, 'Спасибо, данные были внесены в график погашения!', )
            if call.data == 'no':
                start(call.message)

        # Создаем платеж в базе данных
        pay = Payment.objects.create(monthly_payment=100000)
        # Находим последний платеж
        last_pay = Payment.objects.filter().order_by('-payment_date')[0]
        # Находим последний счет
        last_score = Score.objects.filter().order_by('-date_score')[0]
        # Создаем новый счет
        new_score = Score.objects.create(leftover=last_score.leftover - last_pay.monthly_payment,
                                         monthly_payment=last_pay.monthly_payment,
                                         total_payment=last_score.total_payment + last_pay.monthly_payment,
                                         )

        bot.polling(none_stop=True)
