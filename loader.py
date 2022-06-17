from tgbot.config import load_config
from gino import Gino

config = load_config(".env")
db_gino = Gino()

