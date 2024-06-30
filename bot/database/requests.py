from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from bot.database.models import async_session
from bot.database.models import User, Category, Item


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def get_items():
    async with async_session() as session:
        return await session.scalars(select(Item))


async def get_item(item_id: int):
    async with async_session() as session:
        return await session.scalar(select(Item).where(Item.id == item_id))


async def get_items_by_category(category_id: int):
    async with async_session() as session:
        return await session.scalars(select(Item).where(Item.category_id == category_id))


async def set_availability(item_id: int) -> None:
    async with async_session() as session:
        await session.execute(update(Item).where(
            Item.id == item_id).values(availability=False))
        await session.commit()


async def get_human_read_item(item_id: int):
    async with async_session() as session:
        return await session.scalar(select(Item).options(selectinload(Item.category_name)).where(Item.id == item_id))
