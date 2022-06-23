from typing import Optional
from aiogram.dispatcher.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
from tgbot.dal.db_django_commands import get_categories, count_items, get_items
import logging


logger = logging.getLogger()


class ItemsCallbackFactory(CallbackData, prefix="item"):
    level: int
    category: Optional[str]
    sub_category: Optional[str]
    item_id: Optional[int]


class ItemsBuyCallbackFactory(CallbackData, prefix="item"):
    item_id: int


async def categories_keyboard():
    CURRENT_LEVEL = 0
    builder = InlineKeyboardBuilder()
    categories = await get_categories()
    for category in categories:
        count = await count_items(category.category_code)
        builder.button(
            text=f"{category.category_name} ({count})",
            callback_data=ItemsCallbackFactory(level=CURRENT_LEVEL+1,
                                               category=category.category_code
                                               )
        )
    builder.adjust(2)
    return builder.as_markup()


async def items_keyboard(category):
    CURRENT_LEVEL = 1
    builder = InlineKeyboardBuilder()

    items = await get_items(category)
    for item in items:
        builder.button(
            text=f"{item.name} - ${item.price}", callback_data=ItemsCallbackFactory(
                level=CURRENT_LEVEL+1, category=category, item_id=item.id
            )
        )
    builder.button(text="Back", callback_data=ItemsCallbackFactory(level=CURRENT_LEVEL-1, category=category))
    builder.adjust(1)
    return builder.as_markup()


def item_keyboard(category, subcategory, item_id):
    CURRENT_LEVEL = 2
    builder = InlineKeyboardBuilder()
    builder.button(text="Buy", callback_data=ItemsBuyCallbackFactory(item_id=item_id))
    builder.button(text="Back", callback_data=ItemsCallbackFactory(level=CURRENT_LEVEL-1, category=category, subcategory=subcategory))
    builder.adjust(2)
    return builder.as_markup()
