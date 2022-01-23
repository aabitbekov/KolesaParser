import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from kolesaParser import MyParser

API_TOKEN = '5252399024:AAE3MPoa2jFeoifOqCFrJ2AhP3gr9VLT3bY'
# Configure logging
logging.basicConfig(level=logging.INFO)
# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет, я твой персональный помощник по подбору авто!\n"
                        "Хочешь купить машину? Просто напиши /search:")


@dp.message_handler(commands=['search'])
async def chooce(message: types.Message):
    await message.reply("Давайте подберём ваш автомобиль мечты!\nНапишите марку, модель и год авто:")


@dp.message_handler()
async def echo(message: types.Message):
    model = message.text
    model = model.split()
    index = 0

    for m in model:
        model[index] = m.lower()
        index = index + 1
    myParser = MyParser(model[0]+"/"+model[1]+f"?year[from]={model[2]}&year[to]={model[2]}")
    cars = myParser.getCars()
    summa = int(sum(myParser.allPrice) / len(myParser.allPrice))
    top10 = myParser.getSortCars()
    await message.answer(f"[INFO] Всего {len(cars)} товаров удалось собрать...\n "
                         f"Avg price {summa} млн тенге.\n "
                         f"Top ten:\n {top10[0].link}\n"
                         f"{top10[1].link}\n"
                         f"{top10[2].link}\n"
                         f"{top10[3].link}\n"
                         f"{top10[4].link}\n"
                         f"{top10[5].link}\n"
                         f"{top10[6].link}\n"
                         f"{top10[7].link}\n "
                         f"{top10[8].link}\n"
                         f"{top10[9].link}\n")






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)