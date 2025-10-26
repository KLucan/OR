import json
import sqlite3

data = []
companies = {}
genres = {}

con = sqlite3.connect("video_igre.db3")
cur = con.cursor()
for row in cur.execute("SELECT id, name, country_code FROM companies"):
    id, name, country_code = row
    companies.update({id: {"name": name, "country_code": country_code}})
for row in cur.execute("SELECT name, readable_name FROM genres"):
    name, readable_name = row
    genres.update({name: readable_name})
for row in cur.execute("SELECT * FROM games").fetchall():
    id, name, publisher, developer, release_date, score, length = row
    genres = []
    genre_game_query = cur.execute(
        f"SELECT game, readable_name FROM games_genres JOIN genres ON games_genres.genre = genres.name WHERE game = {id}"
    )
    for rrow in genre_game_query:
        _, readable_name = rrow
        genres.append(readable_name)
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
        }
    )
print(json.dumps(data, indent=2))
