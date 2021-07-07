import asyncio
import logging
import time
import json
from aiogram.bot import api
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import admin_id, TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot)


class Contact(StatesGroup):
    name = State()
    bdate = State()
    phone = State()


@dp.message_handler()
async def start(message: types.Message):
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


@dp.message_handler(commands=['add'])
async def add(message: types.Message):
    await message.answer("Введите Имя-Фамилию нового контакта:")
    await Contact.phone.set()


@dp.message_handler(commands=['change'])
async def change():
    pass


@dp.message_handler(commands=['check'])
async def check_closest():
    pass


async def add_name(message: types.Message, state: FSMContext):
    place = message.text.find(' ')
    if place != -1:
        first_name = message.text[:place]
        last_name = message.text[place + 1:]
    else:
        first_name = message.text
        last_name = ''
    await state.update_data(first_name=first_name, last_name=last_name)
    await Contact.next()
    await message.answer(
        "Теперь укажите дату рождения человека (в формате 'дд.мм' или 'дд.мм.гг'. Например:'13.06' или '13.06.1997')"
    )


async def add_bdate(message: types.Message, state: FSMContext):
    appropriate_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    dot, i = 0, 0
    error_msg = "Пожалуйста, используйте только цифры и точку для разделения"
    for char in message.text:
        for a_char in appropriate_chars:
            if char != a_char:
                if char == '.':
                    dot += 1
                    # ADD PROPER VALIDATION OF THE DATE

                    # if dot == 1 and i == 1 or dot == 1 and i == 2 \
                    #         or dot == 2 and i == 5:
                    #     pass
                    # if i < 3 and dot == 1:
                    #     continue
                    continue
                await message.answer(error_msg)
                return
            i += 1
    if dot == 0:
        await message.answer(error_msg)


async def check():
    while True:
        current_day = time.strftime('%d')
        current_month = time.strftime('%m')
        current_date = current_day + '.' + current_month
        message = "Сегодня день рождения отмечает:\n"
        cliche = message
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
                    message += str(i) + ". " + user['first_name'] + " " + user['last_name'] + "\n" + phone + "-" * 5
        if message != cliche:
            # Вместо admin_id соответственно брался бы id пользователя (сейчaс функция абстрагирована)
            await bot.send_message(admin_id, message)
        await asyncio.sleep(86400)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(check())
    executor.start_polling(dp, skip_updates=True)
