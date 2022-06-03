from asyncpg import UniqueViolationError

from tgbot.dal.schemas.user import User
from loader import db_gino


async def add_user(id: int, name: str,email: str = None):
    try:
        user = User(id=id, name=name, email=email)
        await user.create()
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(id: int):
    user = await User.query.where(User.id == id).gino.first()
    return user


async def count_users():
    total = await db_gino.func.count(User.id).gino.scalar()
    return total


async def update_user_email(id , email):
    user = await User.get(id)
    await user.update(email=email).apply()



