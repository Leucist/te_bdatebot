import asyncio
import logging
import time
import json
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
async def check_closest():
    pass


async def check():
    while True:
        current_day = time.strftime('%d')
        current_month = time.strftime('%m')
        current_date = current_day + '.' + current_month
        message = "Сегодня день рождения отмечают:\n"
        # Пока не универсально, а только под меня
        # БД под каждого пользователя были бы "*id-пользователя*.json"
        with open("data.json", "r", encoding="UTF-8") as database:
            data = json.loads(database.read())
            i = 0
            for user in data:
                if current_date == user['bdate'][:5]:
                    i += 1
                    if user['phone'] is not None:
                        phone = user['phone']
                    else:
                        phone = ''
                    message += str(i) + ". " + user['first_name'] + " " + user['last_name'] + "\n" + phone + "-"*5
        await bot.send_message(admin_id, message)
        await asyncio.sleep(86400)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check())
    executor.start_polling(dp, skip_updates=True)
