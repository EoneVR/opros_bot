from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from datetime import datetime

from database import Database
from keyboard import generate_start_button, choose_lang_button, generate_genders_button
from state import Register
from lang import langs


bot = Bot(token='6993946718:AAEQ5CpFsjFj4Ea_unfkQ4FDGeQDoND9hgU')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db = Database()


@dp.message_handler(commands=['start'])
async def command_start(message: Message):
    chat_id = message.chat.id
    db.create_users_table()
    await bot.send_message(chat_id, 'Select language\nВыберите язык\nTilni tanlang', reply_markup=choose_lang_button())


@dp.message_handler(regexp=r'(\🇺🇸 English|\🇷🇺 Русский|\🇺🇿 Ozbek)')
async def get_language_check_progress(message: Message):
    lang = message.text
    chat_id = message.chat.id
    user = db.get_user_by_chat_id(chat_id)
    if lang == '🇷🇺 Русский':
        lang = 'ru'
    elif lang == '🇺🇿 Ozbek':
        lang = 'uz'
    else:
        lang = 'en'
    if user:
        db.set_user_language(chat_id, lang)
    else:
        db.first_register_user(chat_id)
        db.set_user_language(chat_id, lang)
    await message.answer(langs[lang]['select_language'], reply_markup=ReplyKeyboardRemove())
    try:
        with open('images/hackathon.jpg', 'rb') as photo:
            await bot.send_photo(chat_id, photo)
    except FileNotFoundError:
        await bot.send_message(chat_id, "Image not found.")
    await bot.send_message(chat_id, langs[lang]['about'])
    if user:
        if user[2] is None or user[3] is None or user[4] is None or user[5] is None or user[6] is None or user[7] is None:
            await bot.send_message(chat_id, langs[lang]['registration_incomplete'], reply_markup=generate_start_button(lang))
        else:
            await bot.send_message(chat_id, langs[lang]['registration_complete'])
    else:
        await bot.send_message(chat_id, langs[lang]['registration_start'],
                               reply_markup=generate_start_button(lang))


@dp.message_handler(regexp=r"\b(Start registration|Начать регистрацию|Ro'yxatdan o'tishni boshlang)\b")
async def start_register(message: Message):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    await Register.full_name.set()
    await bot.send_message(chat_id, langs[lang]['enter_full_name'], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=Register.full_name)
async def get_full_name_ask_gender(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    await state.update_data(full_name=message.text)
    await Register.gender.set()
    await bot.send_message(chat_id, langs[lang]['choose_gender'], reply_markup=generate_genders_button(lang))


@dp.message_handler(state=Register.gender)
async def get_gender_ask_age(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    await state.update_data(gender=message.text)
    await Register.age.set()
    await bot.send_message(chat_id, langs[lang]['enter_age'], reply_markup=ReplyKeyboardRemove())


@dp.message_handler(regexp='\d\d', state=Register.age)
async def get_age_ask_phone(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    await state.update_data(age=message.text)
    await Register.phone.set()
    await bot.send_message(chat_id, langs[lang]['enter_phone'])


@dp.message_handler(regexp='\+998\d{9}', state=Register.phone)
async def get_phone_ask_occupation(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    await state.update_data(phone=message.text)
    await Register.occupation.set()
    await bot.send_message(chat_id, langs[lang]['position'])


@dp.message_handler(state=Register.occupation)
async def get_occupation_save_data(message: Message, state: FSMContext):
    chat_id = message.chat.id
    lang = db.get_user_language(chat_id)
    occupation = message.text
    data = await state.get_data()
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    db.update_data(chat_id, data['full_name'], data['gender'], data['age'], data['phone'], occupation, time)
    await state.finish()
    await bot.send_message(chat_id, langs[lang]['congratulations'])


@dp.message_handler(commands=['export'])
async def export_data(message: Message):
    chat_id = message.chat.id
    db.save_data_for_excel()
    admin_id = [138104571]
    for admin in admin_id:
        if message.from_user.id == admin:
            with open('users.xlsx', mode='rb') as file:
                await bot.send_document(chat_id, file)
        else:
            await message.answer('Good luck')


executor.start_polling(dp)
