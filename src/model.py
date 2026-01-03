from dataclasses import dataclass, field, fields
from typing import Optional


from db import Db

class ORM():
    
    @classmethod
    def search(cls, list, attribute: str, value: str):
        return [x for x in list if value.lower() in str(getattr(x, attribute)).lower()]

    @classmethod
    def from_db(cls, id: int | str, db: Db):
        return cls(*db.select(cls._table_, (cls._pk_, id), fields(cls)).fetchone())

    @classmethod
    def all_from_db(cls, db: Db):
        return [cls(*x) for x in db.select(cls._table_, fields=fields(cls)).fetchall()]

@dataclass
class Company(ORM):
    _pk_ = "id"
    _table_ = "companies"

    id: int
    name: str
    country_code: str
    parent: int | None

    def __hash__(self):
        return hash(self.id)

@dataclass
class Genre(ORM):
    _pk_ = "name"
    _table_ = "genres"

    name: str
    readable_name: str
    parent: Optional["Genre"]

    def __hash__(self):
        return hash(self.name)

@dataclass
class GameGenre(ORM):
    _pk_ = "game"
    _table_ = "games_genres"

    game: int
    genre: str

    def __hash__(self):
        return hash(f"{self.game}{self.genre}")

@dataclass
class Game(ORM):
    _pk_ = "id"
    _table_ = "games"

    id: int
    name: str
    publisher: int | Company
    developer: int | Company
    release_date: str
    score: Optional["int"]
    length: Optional["float"]
    has_multiplayer: Optional["bool"]
    genres: list[Genre] = field(init=False)

    def __post_init__(self):
        self.genres = 

    def __hash__(self):
        return hash(self.id)
    
    def to_json(self):
        res = {
                "name": row["name"],
                "publisher": {
                    "name": row["publisher-name"],
                    "country-code": row["publisher-country-code"],
                },
                "developer": {
                    "name": row["developer-name"],
                    "country-code": row["developer-country-code"],
                },
                "release-date": row["release-date"],
                "genres": [x for x in row["genres"].split(";")],
                "score": row["score"],
                "length": row["length"],
                "has_multiplayer": row["has_multiplayer"],
              } 

    @classmethod
    def from_db(cls, id: int | str, db: Db):
        raw : Game = super().from_db(id, db)
        raw.publisher = Company.from_db(raw.publisher, db)
        raw.developer = Company.from_db(raw.developer, db)
        return cls(*db.select(cls._table_, (cls._pk_, id), fields(cls)[:-1]).fetchone())

    @classmethod
    def all_from_db(cls, db: Db):
        res : list[Game] = super().all_from_db(db)
        for game in res:
            game.publisher = Company.from_db(game.publisher, db)
            game.developer = Company.from_db(game.developer, db)
        return res