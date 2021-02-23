from django.core.management.base import BaseCommand, CommandError
from server.models import Payment, Score, Lender, Borrower
import telebot
from telebot import types
from urllib.request import urlopen

from .bot_files.extensions import bot, welcome_text


class Command(BaseCommand):
    help = 'Запусти бота'

    temp_int_data = 0

    def handle(self, *args, **options):
        print('starting telegram_bot')

        # Добавить сумму займа
        def add_sum(message):
            if type(int(message.text)) == int:
                text2 = f'Вы ввели сумму {int(message.text)}. Если это верно, то подтвердите:'
                self.temp_int_data = int(message.text)
                keyboard1 = types.InlineKeyboardMarkup()  # Готовим кнопки
                key_yes = types.InlineKeyboardButton(text='Подтвердить', callback_data='yes')
                key_no = types.InlineKeyboardButton(text='Ввести повторно', callback_data='no')
                keyboard1.add(key_yes, key_no)  # И добавляем кнопку на экран
                bot.send_message(message.from_user.id, text2, reply_markup=keyboard1)

        # Добавить пользователей
        def empty_user(message):
            text3 = f'Вам необходимо определить ваш статус:'
            keyboard_stat = types.InlineKeyboardMarkup()  # Готовим кнопки
            key_len = types.InlineKeyboardButton(text='Займодатель', callback_data='lender')
            key_bor = types.InlineKeyboardButton(text='Заемщик', callback_data='borrower')
            keyboard_stat.add(key_len, key_bor)  # И добавляем кнопку на экран
            bot.send_message(message.from_user.id, text3, reply_markup=keyboard_stat)

        # Получить график
        def give_me_report(message):
            text1 = f'Чтобы получить отчет нажмите кнопку:'
            keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
            key_report = types.InlineKeyboardButton(text='Получить график погашения',
                                                    callback_data='give_me_report')
            keyboard.add(key_report)  # И добавляем кнопку на экран
            bot.send_message(message.from_user.id, text1, reply_markup=keyboard)

        @bot.message_handler(commands=['help'])
        def help(message: telebot.types.Message):
            bot.send_message(message.from_user.id, welcome_text)

        @bot.message_handler(commands=['start'])
        def start(message: telebot.types.Message):
            # Проверяем, есть ли запись счетов в базе данных
            if Score.objects.count() == 0:
                text = f"Введите сумму займа:"
                bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(message, add_sum)

            # Определяем пользователя в группу
            elif not Lender.objects.filter(lender=message.from_user.id):
                print('Присваимаем займадателя')
                empty_user(message)
            # Определяем пользователя в группу
            elif not Borrower.objects.filter(borrower=message.from_user.id):
                print('Присваимаем заемщика')
                empty_user(message)

            # Если проверки пройдены, то ничинаем работу
            else:
                text4 = f"Добрый день {message.chat.username}.\nВыберите, что необходимо сделать: \n\n"
                bot.send_message(message.chat.id, text4)
                give_me_report(message)


            # Обработчики нажатия на кнопки
            @bot.callback_query_handler(func=lambda call: True)
            def calbak_worker(call):
                if call.data == 'give_me_report':
                    page = urlopen('http://127.0.0.1:8000/')
                    with open("График.html", "wb") as report:
                        report.write(page.read())
                        print('save')
                    return bot.send_document(call.message.chat.id, open(r'График.html', 'rb'))
                if call.data == 'yes':
                    print(self.temp_int_data)
                    Score.objects.create(total=self.temp_int_data, leftover=self.temp_int_data,
                                         payment_status='подтвержден', monthly_payment=0, total_payment=0, )
                    return bot.send_message(call.message.chat.id, 'Спасибо, данные были внесены в график погашения! \n\n '
                                                           'Для продолжения введите команду /start', )
                if call.data == 'no':
                    return start(call.message)
                if call.data == 'lender':
                    Lender.objects.create(lender=message.from_user.id)
                    bot.send_message(message.from_user.id, 'Спасибо, вы зарегистрированы в качестве Займодателя')
                    print(Borrower.objects.filter(borrower=message.from_user.id))
                    return start(message)
                if call.data == 'borrower':
                    bot.send_message(message.from_user.id, 'Спасибо, вы зарегистрированы в качестве Заемщика')
                    Borrower.objects.create(borrower=message.from_user.id)
                    print(Borrower.objects.filter(borrower=message.from_user.id))
                    return start(message)

        # Создаем платеж в базе данных
        # pay = Payment.objects.create(monthly_payment=100000)
        # # Находим последний платеж
        # last_pay = Payment.objects.filter().order_by('-payment_date')[0]
        # # Находим последний счет
        # last_score = Score.objects.filter().order_by('-date_score')[0]
        # # Создаем новый счет
        # new_score = Score.objects.create(leftover=last_score.leftover - last_pay.monthly_payment,
        #                                  monthly_payment=last_pay.monthly_payment,
        #                                  total_payment=last_score.total_payment + last_pay.monthly_payment,
        #                                  )

        bot.polling(none_stop=True)
