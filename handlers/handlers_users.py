from aiogram import Dispatcher, types
from aiogram.types import Message, ReplyKeyboardMarkup
from aiogram.types.message import ContentType
from create_bot import subscribers, db, connectio, subscriptions
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime, timedelta
from aiogram.types import ChatJoinRequest

from create_bot import dp, bot
from keyboards.kb_users.kb_start import kb_start
from os import getenv

current = datetime.now().date()


async def cmd_start(message: Message):
    await message.answer(text='Это чат с ботом по приобретению подписки', reply_markup=kb_start)


async def buy1(message: types.Message):
    select_price = db.select(subscriptions.columns.price)
    select_subscriptions_name = db.select(subscriptions.columns.subsription_name)
    select_all_price = connectio.execute(select_price).fetchall()
    select_all_name = connectio.execute(select_subscriptions_name).fetchall()
    price1 = types.LabeledPrice(label=f'Подписка на {select_all_name[0][0]}',
                                amount=int(select_all_price[0][0]) * 100)
    price2 = types.LabeledPrice(label=f'Подписка на {select_all_name[1][0]}',
                                amount=int(select_all_price[1][0] * 100))
    durations = db.select(subscriptions.columns.duration)
    select_all_duration = connectio.execute(durations).fetchall()

    await bot.send_invoice(message.chat.id,
                           title='Подписка в закрытый канал',
                           description=f'Доступ в закртый на {select_all_duration[0][0]} дней',
                           provider_token=getenv('TOKEN_PAY'),
                           currency='rub',
                           photo_url='https://noticiast.com/wp-content/uploads/2021/12/Ready-or-not-featured-768x432.jpg',
                           photo_width=768,
                           photo_height=432,
                           photo_size=768,
                           is_flexible=False,
                           prices=[price1],
                           start_parameter=f'one-month-subscription',
                           payload='test-invoice-payload',
                           )

    await bot.send_invoice(message.chat.id,
                           title='Подписка в закрытый канал',
                           description=f'Доступ в закртый на {select_all_duration[1][0]} дней',
                           provider_token=getenv('TOKEN_PAY'),
                           currency='rub',
                           photo_url='https://noticiast.com/wp-content/uploads/2021/12/Ready-or-not-featured-768x432.jpg',
                           photo_width=768,
                           photo_height=432,
                           photo_size=768,
                           is_flexible=False,
                           prices=[price2],
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
    user_id = message.from_user.id
    duration_request = db.select(subscriptions.columns.duration).where(
                                 subscriptions.columns.price == message.successful_payment.total_amount // 100)
    select_duration = connectio.execute(duration_request).fetchall()
    print(select_duration[0][0])
    connectio.execute(subscribers.insert().values(user_id=user_id,
                                                  user_fullname=message.from_user.full_name,
                                                  end_data=datetime.now() + timedelta(days=select_duration[0][0])))
    connectio.commit()


async def cmd_help(message: types.Message):
    await message.answer('Данный бот позволяет приобрести доступ к закрытому тг каналу на 1 месяц, 2 месяца и 3 месяца.'
                         'По вопросам связанными с оплатой и доступом к группе обращайтесь к @username3003')


class FSMUpdateSubscriptions(StatesGroup):
    choosing_to_update = State()
    choosing_parameter_to_update = State()
    name_item_to_update = State()
    duration_item_to_update = State()
    price_item_to_update = State()


# @dp.message_handler(commands='изменение_данных_о_подписке')
async def cmd_update_subscriptions(message: types.Message):
    await FSMUpdateSubscriptions.choosing_to_update.set()
    await message.answer('Укажите количество месяцев той подписки, в которую вы бы хотели внести изменения')


async def choosing_to_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['duration'] = message.text

    await FSMUpdateSubscriptions.next()
    await message.reply('теперь выберете изменяемый параметр',
                        reply_markup=ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
                            'название', 'продолжительность', 'цена'
                        ))


async def choosing_parameter_to_update(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'название':
            await FSMUpdateSubscriptions.name_item_to_update.set()
            await message.answer('укажите новое название')
        elif message.text == 'продолжительность':
            await FSMUpdateSubscriptions.duration_item_to_update.set()
            await message.answer('укажите новую продолжительность')
        elif message.text == 'цена':
            await FSMUpdateSubscriptions.price_item_to_update.set()
            await message.answer('укажите новую стоимость')


async def update_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
        update_query = db.update(subscriptions).where(
            subscriptions.columns.duration == str(data['duration'])).values(
            subsription_name=str(data['name'])
        )
        connectio.execute(update_query)
    connectio.commit()
    await state.finish()


async def update_duration(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['duration1'] = message.text
        update_query = db.update(subscriptions).where(
            subscriptions.columns.duration == str(data['duration'])).values(
            duration=str(data['duration1'])
        )
        connectio.execute(update_query)
        print(data['duration1'])
    connectio.commit()
    await state.finish()


async def update_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text
        update_query = db.update(subscriptions).where(
            subscriptions.columns.duration == str(data['duration'])).values(
            price=float(data['price'])
        )
        connectio.execute(update_query)
    connectio.commit()
    await state.finish()


def register_users_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands='start')
    # dp.register_message_handler(choosing_a_subscription, commands='подписки')
    dp.register_message_handler(buy1, commands=['подписки'])
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda query: True)
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_message_handler(cmd_help, commands=['помощь'])
    dp.register_message_handler(cmd_update_subscriptions, commands=['изменение_данных_о_подписке'])
    dp.register_message_handler(choosing_to_update, state=FSMUpdateSubscriptions.choosing_to_update)
    dp.register_message_handler(choosing_parameter_to_update, state=FSMUpdateSubscriptions.choosing_parameter_to_update)
    dp.register_message_handler(update_name, state=FSMUpdateSubscriptions.name_item_to_update)
    dp.register_message_handler(update_duration, state=FSMUpdateSubscriptions.duration_item_to_update)
    dp.register_message_handler(update_price, state=FSMUpdateSubscriptions.price_item_to_update)