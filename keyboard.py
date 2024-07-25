from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lang import langs


def generate_start_button(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    btn = KeyboardButton(text=langs[lang]['registration_start'])
    markup.add(btn)
    return markup


def choose_lang_button():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    english = KeyboardButton(text='🇺🇸 English')
    russian = KeyboardButton(text='🇷🇺 Русский')
    uzbek = KeyboardButton(text='🇺🇿 Ozbek')
    markup.row(english, russian, uzbek)
    return markup


def generate_genders_button(lang):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    male = KeyboardButton(text=langs[lang]['male'])
    female = KeyboardButton(text=langs[lang]['female'])
    markup.row(male, female)
    return markup

