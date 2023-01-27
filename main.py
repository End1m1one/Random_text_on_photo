import io
import logging
import os
import secrets

import random
import requests as requests

import config

from PIL import Image, ImageDraw
from aiogram import Bot, Dispatcher, executor, types

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.Bot_token)
dp = Dispatcher(bot)

URI_INFO = f"https://api.telegram.org/bot{config.Bot_token}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{config.Bot_token}/"
IMG_NAME = secrets.token_hex(8)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Давай начнем! Для начала отправь мне любое фото",
                           reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types="photo")
async def photo(message: types.Message):
    user_id = message.from_user.id
    file_id = message.photo[3].file_id
    random_text(file_id)
    kb = [
        [types.KeyboardButton(text="Отмена")],
        [types.KeyboardButton(text="Сгенирировать случайную подпись")],
        [types.KeyboardButton(text="Выбрать другую фотографию")]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True
    )
    await bot.send_message(user_id, "Текст придумаешь сам или мне все за тебя делать ?", reply_markup=keyboard)


@dp.message_handler(text="Выбрать другую фотографию")
async def pull_random_text(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Жду от тебя новую фотку", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(text="Отмена")
async def pull_random_text(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Почему передумал?", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(text="Сгенирировать случайную подпись")
async def pull_random_text(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(user_id, "Придумываю подпись")
    await message.answer_photo(photo=open(f'random/{IMG_NAME}.png', 'rb'), reply_markup=types.ReplyKeyboardRemove())


def random_text(file_id):
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI + img_path)
    img = Image.open(io.BytesIO(img.content))
    draw_text = ImageDraw.Draw(img)
    draw_text.text(
        (500, 500),
        text=random_text_to_write(),
        fill='#1C0606'
    )
    if not os.path.exists('random'):
        os.mkdir("random")
    img.save(f'random/{IMG_NAME}.png', format="PNG")


def random_text_to_write():
    phrases = config.phrases
    phrase = random.choice(phrases)
    return phrase


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
