import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.bot import api
from config import admin_id, TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)


@dp.message_handler()
async def start(message: types.Message):
    if message.text:
        await message.answer(
            '''
Привет! Я бот, который может помочь тебе держать под контролем дни рождения всех друзей и знакомых, не забыв никого!
            '''
        )
        await bot.send_message(message.chat.id,
                               '''
Чтобы добавить человека в список, напиши мне "/add"
Чтобы изменить информацию о ком-нибудь, напиши "/change"
Чтобы просмотреть ближайшие дни рождения, напиши "/check"
                               '''
                               )
    else:
        await message.answer("Пожалуйста, пришлите мне текстовое сообщение")


@dp.message_handler(commands=['add'])
async def add():
    pass


@dp.message_handler(commands=['change'])
async def change():
    pass


@dp.message_handler(commands=['check'])
async def check():
    pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
