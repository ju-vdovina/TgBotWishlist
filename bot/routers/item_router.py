from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.formatting import Text, Bold, Italic, Code

import bot.keyboards.keyboards as kb
import bot.database.requests as req

item_router = Router()


def format_price(price):
    return format(price, ',d').replace(',', ' ')


@item_router.callback_query(F.data.startswith('category_'))
async def reply_items_by_category(callback: CallbackQuery):
    await callback.answer('Вы выбрали категорию')

    all_items = await req.get_items_by_category(callback.data.split('_')[1])

    # TODO: Добавить красивое форматирование через встроенные методы aiogram
    # TODO: Добавить пагинацию
    message_answer = '\n\n'.join([f'{'🟢' if item.availability else '🔴'} Название: {item.name}\nЦена: {
        item.price}₽\nПодробная информация: /get{item.id}' for item in all_items])

    await callback.message.answer(message_answer, parse_mode=ParseMode.MARKDOWN)


@item_router.message(F.text.startswith('/get'))
async def reply_item(message: Message):
    item_data = await req.get_human_read_item(message.text[4:])

    message_answer = Text(Bold(f'🌟 {item_data.name}'),
                          Italic(f'\n\n{format_price(item_data.price)} ₽'),
                          '\nСвободно: ',
                          f'{"🟢" if item_data.availability else "🔴"}',
                          '\n\nКатегория: ',
                          Code(f'{item_data.category_name.name}'),
                          f'\nОписание: {item_data.description}',
                          '\nМожно несколько: ',
                          f'{"🟢" if item_data.is_many else "🔴"}'
                          )

    await message.answer(**message_answer.as_kwargs(), reply_markup=await kb.get_item_for_booking(item_data.id))


@item_router.callback_query(F.data.startswith('item_'))
async def reply_book_item(callback: CallbackQuery):
    await callback.answer('Бронирую подарок...')

    item_data = await req.get_item(callback.data.split('_')[1])
    if item_data.availability == False:
        await callback.message.answer('Подарок уже забронирован, но если его можно несколько, то пожалуйста 💞', reply_markup=kb.main_kb)
    else:
        await req.set_availability(item_data.id)
        await callback.message.answer('Подарок забронирован 💞', reply_markup=kb.main_kb)
