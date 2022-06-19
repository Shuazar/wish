from typing import Union

from aiogram import Router
from aiogram.types import Message
from aiogram import types

from tgbot.keyboards.menu_keyboard import categories_keyboard

menu_router = Router()


@menu_router.message(commands=["menu"])
async def cmd_numbers_fab(message: types.Message):
    markup = await categories_keyboard()
    await message.answer(text="טפרית שלנו", reply_markup=markup)
