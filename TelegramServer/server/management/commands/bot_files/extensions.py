from .settings import bot
from telebot import types
from server.models import Payment, Score, Lender, Borrower

welcome_text = f" Вас приветствует бот 7-20-25! Данный бот будет вести учет о погашении " \
               f"займа. В любой момент вы сможете запросить отчет о движении средств."


# кнопка /start
def start_btn(message):
    markup = types.ReplyKeyboardMarkup()
    btn = types.KeyboardButton('/start')
    markup.row(btn)
    bot.send_message(message.from_user.id, 'Для продолжения введите команду /start', reply_markup=markup)
    return


# Добавить пользователей
def empty_user(message):
    text3 = f'Вам необходимо определить ваш статус:'
    keyboard_stat = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_len = types.InlineKeyboardButton(text='Займодатель', callback_data='lender')
    key_bor = types.InlineKeyboardButton(text='Заемщик', callback_data='borrower')
    keyboard_stat.add(key_len, key_bor)  # И добавляем кнопку на экран
    bot.send_message(message.from_user.id, text3, reply_markup=keyboard_stat)


# Получить график
def give_me_report(message, args=0):
    text1 = f'Чтобы получить отчет нажмите кнопку:'
    keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_report = types.InlineKeyboardButton(text='Получить график погашения',
                                            callback_data='give_me_report')
    keyboard.add(key_report)  # И добавляем кнопку на экран
    if args == 0:
        bot.send_message(message.from_user.id, text1, reply_markup=keyboard)
    else:
        bot.send_message(args, text1, reply_markup=keyboard)


# Сделать платеж
def make_payment(message):
    text = f'Отправить уведомление о переводе:'
    keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_send = types.InlineKeyboardButton(text='Сумма перевода', callback_data='send_money')
    keyboard.add(key_send)  # И добавляем кнопку на экран
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


# Выбрать сумму перевода
def choice_sum(message):
    text = f'Выберите сумму:'
    keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_50 = types.InlineKeyboardButton(text='50 000', callback_data='50')
    key_100 = types.InlineKeyboardButton(text='100 000', callback_data='100')
    key_200 = types.InlineKeyboardButton(text='другое', callback_data='other')
    keyboard.add(key_50, key_100, key_200)  # И добавляем кнопку на экран
    bot.send_message(message.from_user.id, text, reply_markup=keyboard)


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
    print('Изменения успешно внесены в график погашения')


# Отчет об отправке уведомления
def confirm_send_payment(message, args: int):
    lender_id = Lender.objects.all()[0].lender_id
    text = f'Вам пришло уведомление о переводе средств на карту в размере {args} тг'
    keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_yes = types.InlineKeyboardButton(text='Подтвердить', callback_data='yes_arrive')
    key_no = types.InlineKeyboardButton(text='Отклонить', callback_data='no_arrive')
    keyboard.add(key_yes, key_no)  # И добавляем кнопку на экран
    bot.send_message(lender_id, text, reply_markup=keyboard)
    bot.send_message(message.from_user.id, 'Уведомление о переводе средств успешно отправлено')


# Подтверждение о поступлении
def yes_arrive(message):
    # Находим последний счет
    last_score = Score.objects.filter().order_by('-date_score')[0]
    last_score.payment_status = 'подтверждено'
    last_score.save()
    lender_id = Lender.objects.all()[0].lender_id
    borrower_id = Borrower.objects.all()[0].borrower_id
    bot.send_message(lender_id, 'Подтверждено', )
    bot.send_message(borrower_id, 'Подтверждено', )
    start_btn(message)


# Отклонить поступление
def no_arrive(call):
    text = f'Вы собираетесь отклонить запрос, вы уверены?'
    keyboard = types.InlineKeyboardMarkup()  # Готовим кнопки
    key_yes = types.InlineKeyboardButton(text='Да, отклоняю', callback_data='go_back')
    key_no = types.InlineKeyboardButton(text='Нет, нужно проверить', callback_data='check')
    keyboard.add(key_yes, key_no)  # И добавляем кнопку на экран
    bot.send_message(call.from_user.id, text, reply_markup=keyboard)


# Отправить свою сумму перевода
def other_sum(message):
    text = 'Введите сумму перевода:'
    bot.send_message(message.from_user.id, text)
