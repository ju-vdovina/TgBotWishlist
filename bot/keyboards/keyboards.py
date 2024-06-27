from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

import bot.database.requests as req

main_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Поиграть в "рулетку"'),
                                         KeyboardButton(
                                             text='Выбрать категорию'),
                                         KeyboardButton(text='Ближайшие ПВЗ')]],
                              resize_keyboard=True,
                              input_field_placeholder='Выберите пункт меню')


async def categories_kb():
    all_categories = await req.get_categories()
    keyboard = InlineKeyboardBuilder()
    for category in all_categories:
        keyboard.add(InlineKeyboardButton(text=category.name,
                     callback_data=f"category_{category.id}"))
    return keyboard.adjust(2).as_markup()


async def get_item_for_booking(item_id):
    item_data = await req.get_item(item_id)
    keyboard = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text='Забронировать',
                 callback_data=f"item_{item_data.id}"))

    return keyboard.as_markup()
