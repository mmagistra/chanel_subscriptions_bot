from create_bot import bot
from aiogram import Bot, types, Dispatcher
from create_bot import subscribers, connectio, db
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMMalling(StatesGroup):
    message_for_mailing = State()
    photo_for_malling = State()


async def cmd_malling(message: types.Message):
    await FSMMalling.message_for_mailing.set()
    await message.reply('Введите информацию для рассылки')


async def message_for_malling(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['malling'] = message.text
        await FSMMalling.next()
        await message.reply('Отправьте изображение для рассылки')


async def photo_for_malling(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id
        select_all_query = db.select(subscribers.columns.user_id)
        select_all_result = connectio.execute(select_all_query).fetchall()
        for user_id in select_all_result:
            await bot.send_photo(user_id[0], photo=data['photo'], caption=data['malling'])
    await state.finish()


def register_malling_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_malling, commands=['рассылка'], state='*')
    dp.register_message_handler(message_for_malling, state=FSMMalling.message_for_mailing)
    dp.register_message_handler(photo_for_malling,content_types=types.ContentType.PHOTO, state=FSMMalling.photo_for_malling)





