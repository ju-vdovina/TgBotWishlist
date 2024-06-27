import random
import os
from dotenv import load_dotenv

from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.enums.parse_mode import ParseMode

import bot.keyboards.keyboards as kb
import bot.database.requests as req

random.seed(2024)
load_dotenv()
main_router = Router()


@main_router.message(CommandStart())
async def reply_start_command(message: Message):
    await req.set_user(message.from_user.id)
    message_answer = f'Привет, {
        message.from_user.username}!\nНажми /help, если потерялся.'
    await message.answer(message_answer, reply_markup=kb.main_kb)


@main_router.message(Command('help'))
async def reply_help_command(message: Message):
    message_answer = 'Здесь можно выбрать и забронить подарочек. Нажимай кнопки на клавиатуре внизу'
    await message.answer(message_answer, reply_markup=kb.main_kb)


@main_router.message(F.text == 'Поиграть в "рулетку"')
async def send_dice(message: Message):
    await message.answer_dice(emoji=random.choice(['🎳', '🎯', '🏀', '🎰', '🎲']))


@main_router.message(F.text == 'Ближайшие ПВЗ')
async def reply_pvz_links(message: Message):
    message_answer = f"""🍀 [Ozon]({os.getenv('OZON_PVZ')})\n🍀 [Яндекс Маркет]({
        os.getenv('YA_MARKET_PVZ')})"""
    await message.answer(message_answer, reply_markup=kb.main_kb, parse_mode=ParseMode.MARKDOWN)


@main_router.message(F.text == 'Выбрать категорию')
async def reply_categories(message: Message):
    message_answer = 'Выберите категорию товара'
    await message.answer(message_answer, reply_markup=await kb.categories_kb())


@main_router.message()
async def reply_any_message(message: Message):
    message_answer = 'Я не могу ответить на такое. Пожалуйста, выбери кнопку на клавиатуре🙏'
    await message.answer(message_answer, reply_markup=kb.main_kb)
