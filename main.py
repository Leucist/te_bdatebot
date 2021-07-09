import asyncio
import logging
import time
import json
from aiogram import Bot, Dispatcher, executor, types
#
from aiogram.contrib.fsm_storage.memory import MemoryStorage
#
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from config import admin_id, TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


class Contact(StatesGroup):
    name = State()
    bdate = State()
    phone = State()


@dp.message_handler(commands="add", state="*")
async def cmd_add(message: types.Message, state: FSMContext):
    await state.finish()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('/cancel')
    new_message = '''
Для начала необходимо будет указать некоторые данные нового контакта.
Если Вы захотите прекратить процесс, можете написать команду "/cancel" в любой момент.

Введите Имя-Фамилию нового контакта:
'''
    await message.answer(new_message, reply_markup=markup)
    await Contact.name.set()


@dp.message_handler(commands="cancel", state="*")
async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())


# def register_handlers(dp: Dispatcher):
#     dp.register_message_handler(cmd_add, commands="add", state="*")
#     dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
#     dp.register_message_handler(add_name, state=Contact.name)
#     dp.register_message_handler(add_bdate, state=Contact.bdate)
#     dp.register_message_handler(add_phone, state=Contact.phone)


@dp.message_handler(commands=['change'])
async def change():
    pass


@dp.message_handler(commands=['check'])
async def check_closest():
    pass


@dp.message_handler(state=Contact.name)
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


@dp.message_handler(state=Contact.bdate)
async def add_bdate(message: types.Message, state: FSMContext):
    appropriate_chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    dot, i = 0, 0
    error_msg = "Пожалуйста, используйте только цифры и точку для разделения"
    for char in message.text:
        for a_char in appropriate_chars:
            if char == a_char:
                continue
        ## Still need to be fixed

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
        return
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add('/finish')
        await state.update_data(bdate=message.text)
        await Contact.next()
        await message.answer("Укажите номер телефона для нового контакта.\nЕсли такого нет, напишите '/finish'",
                             reply_markup=markup)


@dp.message_handler(state=Contact.phone)
async def add_phone(message: types.Message, state: FSMContext):
    if message.text == "/finish":
        await state.update_data(phone=None)
    else:
        await state.update_data(phone=message.text)
    contact = await state.get_data()
    with open("data.json", "r", encoding="UTF-8") as database:
        data = json.loads(database.read())
        for user in data:
            if user['first_name'] == contact['first_name']:
                if user['last_name'] == contact['last_name']:
                    await message.answer("Контакт с такими данными уже существует.",
                                         reply_markup=types.ReplyKeyboardRemove())
                    break
        else:
            data.append({
                "first_name": contact['first_name'],
                "last_name": contact['last_name'],
                "bdate": contact['bdate'],
                "phone": contact['phone']
            })
            await save_data(data, "data.json")
            await message.answer("Контакт успешно сохранен.", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


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
                    message += str(i) + ". " + user['first_name'] + " " + user[
                        'last_name'] + "\n" + phone + "-" * 16 + "\n"
        if message != cliche:
            # Вместо admin_id соответственно брался бы id пользователя (сейчaс функция абстрагирована)
            await bot.send_message(admin_id, message)
        await asyncio.sleep(86400)


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


async def save_data(data, filename):
    with open(filename, "w", encoding="UTF-8") as database:
        json.dump(data, database, indent=1, ensure_ascii=False, separators=(',', ':'))


if __name__ == '__main__':
    # register_handlers(dp)
    loop = asyncio.get_event_loop()
    loop.create_task(check())
    executor.start_polling(dp, skip_updates=True)
