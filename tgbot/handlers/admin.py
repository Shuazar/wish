import asyncpg.exceptions
from aiogram import Router
from aiogram.types import Message
from loader import db

from tgbot.dal.postgresql import Database
from tgbot.filters.admin import AdminFilter

admin_router = Router()
#admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["start"], state="*")
async def admin_start(message: Message):
    try:
        user = await db.add_user(
            full_name=message.from_user.full_name,
            username=message.from_user.username,
            telegram_id = message.from_user.id,
        )
    except asyncpg.exceptions.UniqueViolationError:
        user = await db.select_user(telegram_id=message.from_user.id)

    count_users = await db.count_users()
    user_data = list(user)
    user_data_dict = dict(user)

    user_name = user.get('username')
    full_name = user[2]

    await message.answer(
        "\n".join(
            [
                f'Hi, {message.from_user.full_name}!'
                f'You are was added to database'
                f'In database <b>{count_users}</b> users'
            ]
        )
    )
    await message.reply("Hi, admin!")
