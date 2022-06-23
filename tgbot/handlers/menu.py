from contextlib import suppress
from typing import Union
import logging
from aiogram import Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from aiogram import types

from tgbot.dal.db_django_commands import get_item
from tgbot.keyboards.menu_keyboard import categories_keyboard, items_keyboard, item_keyboard, ItemsCallbackFactory

menu_router = Router()

logger = logging.getLogger()


@menu_router.message(commands=["menu"])
async def cmd_numbers_fab(message: types.Message):
    await list_categories(message)


async def list_categories(message: Union[Message, CallbackQuery], **kwargs):
    with suppress(TelegramBadRequest):
        logger.info("----------------list_categories----------------------")
        markup = await categories_keyboard()

        if isinstance(message, Message):
            await message.answer(text="טפרית שלנו", reply_markup=markup)

        elif isinstance(message, CallbackQuery):
            call = message
            await call.message.edit_reply_markup(markup)


async def list_items(callback: CallbackQuery, category,  **kwargs):
    with suppress(TelegramBadRequest):
        logger.info("-------------------list_items-------------------Items")
        markup = await items_keyboard(category=category)
        await callback.message.edit_text(text="\U00002b07 בחר אחד מהפריטים ", reply_markup=markup)


async def show_item(callback: CallbackQuery, category, subcategory, item_id):
    with suppress(TelegramBadRequest):
        logger.info("-----------------show_item---------------------")
        markup = item_keyboard(category, subcategory, item_id)

        item = await get_item(item_id)
        text = f"Buy {item}"
        await callback.message.edit_text(text, reply_markup=markup)


@menu_router.callback_query(ItemsCallbackFactory.filter())
async def navigate(call: CallbackQuery, callback_data: ItemsCallbackFactory):
    current_level = callback_data.level
    category = callback_data.category
    subcategory = callback_data.sub_category
    item_id = callback_data.item_id

    logger.info(f"Level --------- {current_level}")
    logger.info(f"category --------- {category}")
    logger.info(f"subcategory --------- {subcategory}")
    logger.info(f"item_id --------- {item_id}")
    if current_level == 0:
        await list_categories(call, category=category, subcategory=subcategory, item_id=item_id)
    elif current_level == 1:
        await list_items(call, category=category, subcategory=subcategory, item_id=item_id)
    else:
        await show_item(call, category=category, subcategory=subcategory, item_id=item_id)