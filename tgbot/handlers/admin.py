import asyncpg.exceptions
from aiogram import Router
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.markdown import hcode

from loader import db

from tgbot.dal.postgresql import Database
from tgbot.filters.admin import AdminFilter

admin_router = Router()
#admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["start_db"], state="*")
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
    full_name = user[1]

    await message.answer(
        "\n".join(
            [
                f'Hi, {message.from_user.full_name}!\n'
                f'You are was added to database\n'
                f'In database <b>{count_users}</b> users',
                "",
                f"<code>User: {user_name} - {full_name}",
                f"{user_data}",
                f"{user_data_dict=}</code>"
            ]
        )
    )
    await message.reply("Hi, admin!")


@admin_router.message(commands=["username"])
async def change_username(message: Message, state:FSMContext):
    await message.answer("Send me new user name")
    await state.set_state("username")


@admin_router.message(state="username")
async def enter_username(message: Message, state: FSMContext):
    await db.update_user_username(username=message.text, telegram_id=message.from_user.id)
    user = await db.select_user(telegram_id=message.from_user.id)
    user = dict(user)
    await message.answer("Info was updated. Row into DB:\n"+
                         hcode(
                             f"{user=}"
                         ))
    await state.clear()

