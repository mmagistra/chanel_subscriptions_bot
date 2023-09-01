from os import getenv

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.types.message import ContentType

from create_bot import dp, bot
from keyboards.kb_users.kb_start import kb_start
from os import getenv


@dp.message_handler(commands='start')
async def cmd_start(message: Message):
    await message.answer(text='Это чат с ботом по приобретению подписки', reply_markup=kb_start)


PRICE = types.LabeledPrice(label='Подписка на 1 месяц', amount=500 * 100)


async def buy(message: types.Message):
    if str(getenv('PAYMENTS_TOKEN')).split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'Тестовый платёж!')
    await bot.send_invoice(message.chat.id,
                           title='Подписка в закрытый канал',
                           description='Доступ в закртый на 1 месяц',
                           provider_token=str(getenv('PAYMENTS_TOKEN')),
                           currency='rub',
                           photo_url='https://noticiast.com/wp-content/uploads/2021/12/Ready-or-not-featured-768x432.jpg',
                           photo_width=768,
                           photo_height=432,
                           photo_size=768,
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter='one-month-subscription',
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


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    dp.register_message_handler(buy, commands=['подписки'])
    dp.register_message_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
