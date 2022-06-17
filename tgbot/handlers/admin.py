from aiogram import Router, Bot
from tgbot.dal import db_django_commands as commands
from aiogram.types import Message
admin_router = Router()
#admin_router.message.filter(AdminFilter())


@admin_router.message(commands=["dice"])
async def send_dice(message: Message, bot: Bot):
    await bot.send_dice(message.from_user.id)



@admin_router.message(commands=["start_django"], state="*")
async def add_new_user(message: Message):
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
