from aiogram import Router, Bot
from aiogram.types import Message
from tgbot.dal import db_django_commands as commands
from tgbot.handlers.admin import send_income_user
start_router = Router()


@start_router.message(commands=["start"])
async def bot_start(message: Message, bot: Bot):
    user = await commands.add_user(user_id=message.from_user.id,
                                   full_name=message.from_user.full_name,
                                   username=message.from_user.username)
    await message.answer(
        "\n".join([
            f'Hi, {message.from_user.full_name}',
            f'We welcome you to our store'
        ])
    )
    await message.answer(f'Hi, {message.from_user.full_name}! '
                         f'press /menu')
    await send_income_user(message, bot)


