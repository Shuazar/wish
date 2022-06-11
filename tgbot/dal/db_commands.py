import os
from typing import List

import django
from asyncpg import UniqueViolationError

from django_project.wish.wish_admin.models import Item, User
from asgiref.sync import sync_to_async


@sync_to_async
def select_user(user_id: int):
    user = User.objects.filter(user_id=user_id).first()
    return user


@sync_to_async
def add_user(user_id, username, full_name):
    try:
        User(user_id=int(user_id), username=username, fullname=full_name).save()
    except UniqueViolationError:
        pass


@sync_to_async
def get_all_users():
    users = User.objects.all()
    return users


@sync_to_async
def count_users():
    return User.objects.all().count()


@sync_to_async
def add_item(**kwargs):
    newitem = Item(**kwargs).save()
    return newitem


@sync_to_async
def get_categories() -> List[Item]:
    return Item.objects.distinct("category_name").all()


@sync_to_async
def get_subcategories(category_code) -> List[Item]:
    return Item.objects.distinct("subcategory_name").filter(category_code=category_code).all()


@sync_to_async
def count_items(category_code, subcategory_code=None) -> int:
    conditions = dict(category_code=category_code)
    if subcategory_code:
        conditions.update(subcategory_code=subcategory_code)

    return Item.objects.filter(**conditions).count()


@sync_to_async
def get_items(category_code, subcategory_code) -> List[Item]:
    return Item.objects.filter(category_code=category_code, subcategory_code=subcategory_code).all()


@sync_to_async
def get_item(item_id) -> Item:
    return Item.objects.filter(id=int(item_id)).first()
