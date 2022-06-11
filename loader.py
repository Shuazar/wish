import os

import django

from tgbot.config import load_config
from tgbot.dal.postgresql import Database
from gino import Gino

config = load_config(".env")
db = Database()
db_gino = Gino()

