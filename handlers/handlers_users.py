from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ReplyKeyboardMarkup
from aiogram.types.message import ContentType
from create_bot import subscribers, db, connectio
from datetime import datetime


from create_bot import dp, bot
from keyboards.kb_users.kb_start import kb_start
from os import getenv

current = datetime.now().date()


async def cmd_start(message: Message):
    await message.answer(text='Это чат с ботом по приобретению подписки', reply_markup=kb_start)
    # insertion_query = subscribers.insert().values(user_id=message.from_user.id,
    #                                               user_fullname=message.from_user.full_name,
    #                                               end_data=current)
    # connectio.execute(insertion_query)
    # connectio.commit()
    # print(subscribers)
    # print('пользователь добавлен')


PRICE1 = types.LabeledPrice(label='Подписка на 1 месяц', amount=500 * 100)
PRICE2 = types.LabeledPrice(label='Подписка на 2 месяца', amount=1000 * 100)


async def buy1(message: types.Message):
    if getenv('TOKEN_PAY').split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Тестовый платёж!')
    await bot.send_invoice(message.chat.id,
                           title='Подписка в закрытый канал',
                           description='Доступ в закртый на 1 месяц',
                           provider_token=getenv('TOKEN_PAY'),
                           currency='rub',
                           photo_url='https://noticiast.com/wp-content/uploads/2021/12/Ready-or-not-featured-768x432.jpg',
                           photo_width=768,
                           photo_height=432,
                           photo_size=768,
                           is_flexible=False,
                           prices=[PRICE1],
                           start_parameter='one-month-subscription',
                           payload='test-invoice-payload')

    if getenv('TOKEN_PAY').split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Тестовый платёж!')
    await bot.send_invoice(message.chat.id,
                           title='Подписка в закрытый канал',
                           description='Доступ в закртый на 2 месяц',
                           provider_token=getenv('TOKEN_PAY'),
                           currency='rub',
                           photo_url='https://noticiast.com/wp-content/uploads/2021/12/Ready-or-not-featured-768x432.jpg',
                           photo_width=768,
                           photo_height=432,
                           photo_size=768,
                           is_flexible=False,
                           prices=[PRICE2],
                           start_parameter='two-month-subscription',
                           payload='test-invoice-payload')


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


async def successful_payment(message: types.Message):
    print('SUCCESSFUL PAYMENT:')
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        print(f'{k} = {v}')

    await bot.send_message(message.chat.id,
                           f'''Платёж на сумму {message.successful_payment.total_amount // 100} 
{message.successful_payment.currency} прошёл успешно!!!''')


async def cmd_help(message: types.Message):
    await message.answer('Данный бот позволяет приобрести доступ к закрытому тг каналу на 1 месяц, 2 месяца и 3 месяца.'
                         'По вопросам связанными с оплатой и доступом к группе обращайтесь к @username3003')


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    # dp.register_message_handler(choosing_a_subscription, commands='подписки')
    dp.register_message_handler(buy1, commands=['подписки'])
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(cmd_help, commands=['помощь'])
