import io
import logging
import os
import secrets

import requests as requests
from PIL import Image, ImageFilter
from aiogram.types import ContentType

from config import Bot_token
from aiogram import Bot, Dispatcher, executor, types


logging.basicConfig(level=logging.INFO)
MSG = 'Hello, {}'
bot = Bot(token=Bot_token)
dp = Dispatcher(bot)
URI_INFO = f"https://api.telegram.org/bot{Bot_token}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{Bot_token}/"

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    logging.info(f'{user_name}, {user_id}')
    await bot.send_message(user_id, MSG.format(user_name))

@dp.message_handler(content_types=['photo'])
async def photo(message: types.Message):
    file_id = message.photo[3].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI + img_path)
    img = Image.open(io.BytesIO(img.content))
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    if not os.path.exists('static'):
        os.mkdir('static')
    img_name = secrets.token_hex(8)
    img.save(f'static/{img_name}.png', format="PNG")
    await message.answer_photo(photo=open(f'static/{img_name}.png', 'rb'))



if __name__ == '__main__':
    executor.start_polling(dp)