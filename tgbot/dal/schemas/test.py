import asyncio

from loader import db_gino, config
from tgbot.dal.schemas import quick_commands


async def test():
    await db_gino.set_bind(config.db.postgres_uri)
    await db_gino.gino.drop_all()
    await db_gino.gino.create_all()

    print("Adding users")
    await quick_commands.add_user(1, "One", "Email")

loop = asyncio.get_event_loop()
loop.run_until_complete(test())