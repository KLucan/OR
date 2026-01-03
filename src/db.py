import sqlite3
from dataclasses import fields, asdict

class Db():
    con: sqlite3.Connection
    cur: sqlite3.Cursor

    def __init__(self, path: str = "../video_igre.db3"):
        self.con = sqlite3.connect("../video_igre.db3")
        self.cur = self.con.cursor()

    def execute(self, sql: str, parameters = (), /):
        return self.cur.execute(sql)
    
    def select(self, table: str, single: tuple[str, int] | tuple[str, str]=["",""], fields: list | str="*"):
        where_clause = ""
        if single[0] and single[1]:
            where_clause = f" WHERE {single[0]} = {single[1]}"
        if type(fields) == type(str):
            return self.execute(f"SELECT {fields} FROM {table}{where_clause}")
        else:
            return self.execute(f"SELECT {", ".join([x.name for x in fields])} FROM {table}{where_clause}")

    def get_data(self, flat=False):
        data = []
        companies = {}
        genres = {}

        for row in self.execute("SELECT id, name, country_code FROM companies"):
            id, name, country_code = row
            companies.update({id: {"name": name, "country_code": country_code}})
        for row in self.execute("SELECT name, readable_name FROM genres"):
            name, readable_name = row
            genres.update({name: readable_name})
        for row in self.execute("SELECT * FROM games").fetchall():
            id, name, publisher, developer, release_date, score, length, has_multiplayer = row
            genres = []
            genre_game_query = self.execute(
                f"SELECT game, readable_name FROM games_genres JOIN genres ON games_genres.genre = genres.name WHERE game = {id}"
            )
            for rrow in genre_game_query:
                _, readable_name = rrow
                genres.append(readable_name)
            if flat:
                data.append(
                    {
                        "name": name,
                        "publisher-name": companies[publisher]["name"],
                        "publisher-country-code": companies[publisher]["country_code"],
                        "developer-name": companies[developer]["name"],
                        "developer-country-code": companies[developer]["country_code"],
                        "release-date": release_date,
                        "genres": ";".join(genres),
                        "score": score,
                        "length": length,
                        "has_multiplayer": has_multiplayer,
                    }
                )
            else:
                data.append(
                    {
                        "name": name,
                        "publisher": {
                            "name": companies[publisher]["name"],
                            "country-code": companies[publisher]["country_code"],
                        },
                        "developer": {
                            "name": companies[developer]["name"],
                            "country-code": companies[developer]["country_code"],
                        },
                        "release-date": release_date,
                        "genres": genres,
                        "score": score,
                        "length": length,
                        "has_multiplayer": bool(has_multiplayer),
                    }
                )
        return data