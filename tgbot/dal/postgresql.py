from typing import Union
import logging
import asyncpg
from asyncpg import Connection

from tgbot.config import load_config
from asyncpg.pool import Pool


config = load_config(".env")


class Database:

    def __init__(self):
        self.pool: Union[Pool] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.db.user,
            password=config.db.password,
            host=config.db.host,
            database=config.db.database
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
           CREATE TABLE IF NOT EXISTS students (
           id SERIAL PRIMARY KEY,
           full_name VARCHAR(255) NOT NULL,
           username varchar(255) NULL,
           telegram_id BIGINT NOT NULL UNIQUE 
           );
           """
        await self.execute(sql, execute=True)
        logging.info(config.db.postgres_uri)

    async def select_all_users(self):
        sql = "SELECT * FROM students"
        return await self.execute(sql,fetch=True)

    @staticmethod
    def format_args(sql, parameters:dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num , item in enumerate(parameters.keys(), start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO students (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM students WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM students"
        return await self.execute(sql,fetch=True)

    async def count_users(self):
        sql = "SELECT * FROM students"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

