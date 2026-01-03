from fasthtml.common import *
from scripts.export_json import export_json
from scripts.export_csv import export_csv
from db import Db
from model import *

db = Db()
games: list[Game] = Game.all_from_db(db)
games = Game.search(games, "name", "dish")
print(games)