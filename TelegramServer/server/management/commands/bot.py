from .bot_files.extensions import *
from django.core.management.base import BaseCommand, CommandError
from server.models import Payment, Score, Lender, Borrower
import telebot
from telebot import types
from urllib.request import urlopen


class Command(BaseCommand):
    help = 'Запусти бота'

    temp_int_data = 0

    def handle(self, *args, **options):
        print('starting telegram_bot')

        # Сделать платеж
        def make_payment(message):
            text1 = f'Отправить уведомление о переводе:'
            keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
            key_send = types.InlineKeyboardButton(text='Сумма перевода',
                                                  callback_data='send_money')
            keyboard.add(key_send)  # И добавляем кнопку на экран
            bot.send_message(message.from_user.id, text1, reply_markup=keyboard)

        # Выбрать сумму перевода
        def choice_sum(message):
            text1 = f'ВЫберите сумму:'
            keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
            key_50 = types.InlineKeyboardButton(text='50 000', callback_data='50')
            key_100 = types.InlineKeyboardButton(text='100 000', callback_data='100')
            key_150 = types.InlineKeyboardButton(text='150 000', callback_data='150')
            key_200 = types.InlineKeyboardButton(text='другое', callback_data='other')
            keyboard.add(key_50, key_100, key_150, key_200)  # И добавляем кнопку на экран
            bot.send_message(message.from_user.id, text1, reply_markup=keyboard)

        # Внести изменения в график погашения
        def new_report(payment: int):
            # Создаем платеж в базе данных
            Payment.objects.create(monthly_payment=payment)
            # Находим последний платеж
            last_pay = Payment.objects.filter().order_by('-payment_date')[0]
            # Находим последний счет
            last_score = Score.objects.filter().order_by('-date_score')[0]
            # Создаем новый счет
            Score.objects.create(total=last_score.total, leftover=last_score.leftover - last_pay.monthly_payment,
                                 monthly_payment=last_pay.monthly_payment,
                                 total_payment=last_score.total_payment + last_pay.monthly_payment,
                                 )
            print('Изменения успешно внесены в базу данных')

        # Отчет об отправке уведомления
        def confirm_send_payment(message):

            bot.send_message(message.from_user.id, 'Уведомление о переводе средств успешно отправлено')




            # Отправить свою сумму перевода
        def other_sum(message):
            text = 'Введите сумму перевода:'
            bot.send_message(message.from_user.id, text)

        # Принять другую сумму
        def confirm_other_sum(message):
            if type(int(message.text)) == int:
                text2 = f'Вы ввели сумму {int(message.text)}. Если это верно, то подтвердите:'
                self.temp_int_data = int(message.text)
                keyboard1 = types.InlineKeyboardMarkup()  # Готовим кнопки
                key_yes = types.InlineKeyboardButton(text='Подтвердить', callback_data='other_yes')
                key_no = types.InlineKeyboardButton(text='Ввести повторно', callback_data='other_no')
                keyboard1.add(key_yes, key_no)  # И добавляем кнопку на экран
                bot.send_message(message.from_user.id, text2, reply_markup=keyboard1)


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

            lenders = Lender.objects.filter(lender=message.from_user.id)  # займодатель
            print(lenders)
            borrowers = Borrower.objects.filter(borrower=message.from_user.id)  # заемщик
            print(borrowers)

            # Проверяем, есть ли запись счетов в базе данных
            if Score.objects.count() == 0:
                text = f"Введите сумму займа:"
                bot.send_message(message.chat.id, text)
                bot.register_next_step_handler(message, add_sum)

            # Определяем пользователя
            elif not lenders:
                # Если это бороуер то выполняет работу
                if borrowers:
                    make_payment(message)
                    give_me_report(message)
                else:
                    print('Присваимаем займадателя')
                    empty_user(message)
            # Определяем пользователя
            elif not borrowers:
                # Если это лендер то выполняет работу
                if lenders:
                    give_me_report(message)
                else:
                    print('Присваимаем заемщика')
                    empty_user(message)



            # Обработчики нажатия на кнопки
            @bot.callback_query_handler(func=lambda call: True)
            def calbak_worker(call):
                if call.data == 'give_me_report':
                    page = urlopen('http://127.0.0.1:8000/')
                    with open("График.html", "wb") as report:
                        report.write(page.read())
                        print('save')
                    return bot.send_document(call.message.chat.id, open(r'График.html', 'rb'))

                elif call.data == 'send_money':
                    choice_sum(message)
                elif call.data == '50':
                    new_report(50000)
                elif call.data == '100':
                    new_report(100000)
                elif call.data == '150':
                    new_report(150000)
                    bot.register_next_step_handler(call.message, confirm_send_payment)
                elif call.data == 'other':
                    other_sum(message)
                    bot.register_next_step_handler(call.message, confirm_other_sum)

                elif call.data == 'other_yes':
                    new_report(self.temp_int_data)




                elif call.data == 'other_no':
                    new_report(self.temp_int_data)

                if call.data == 'yes':
                    Score.objects.create(total=self.temp_int_data, leftover=self.temp_int_data,
                                         payment_status='подтвержден', monthly_payment=0, total_payment=0, )
                    return bot.send_message(call.message.chat.id,
                                            'Спасибо, данные были внесены в график погашения! \n\n '
                                            'Для продолжения введите команду /start', )
                if call.data == 'no':
                    return start(call.message)
                if call.data == 'lender':
                    if not lenders:
                        Lender.objects.create(lender=message.from_user.id)
                        bot.send_message(message.from_user.id, 'Спасибо, вы зарегистрированы в качестве Займодателя')
                    else:
                        bot.send_message(message.from_user.id, 'Займодатель ранее был зарегистрирован')
                    return start(message)
                if call.data == 'borrower':
                    if not borrowers:
                        bot.send_message(message.from_user.id, 'Спасибо, вы зарегистрированы в качестве Заемщика')
                        Borrower.objects.create(borrower=message.from_user.id)
                    else:
                        bot.send_message(message.from_user.id, 'Заемщик ранее был зарегистрирован')
                    return start(message)

        bot.polling(none_stop=True)
