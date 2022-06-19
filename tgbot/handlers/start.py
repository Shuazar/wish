from aiogram import  Router
from aiogram.types import Message
from tgbot.dal import db_django_commands as commands

start_router = Router()


@start_router.message(commands=["start"])
async def bot_start(message: Message):
    await message.answer(f'Hi, {message.from_user.full_name}! '
                         f'press /menu')
    user = await commands.add_user(user_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username)

    count = await commands.count_users()
    await message.answer(
        "\n".join([
            f'Hi, {message.from_user.full_name}',
            f'You are was added to database',
            f'In database <b>{count}</b> users'
        ])
    )
