from fastlite import *

def dump():
    db = database("../video_igre.db3")
    games = db.t.games
    return games()

def get_game(id: int):
    db = database("../video_igre.db3")
    games = db.t.games
    try:
        res = games[id]
        return res
    except NotFoundError:
        return None

def get_game_genre(genre: str = "None"):
    db = database("../video_igre.db3")
    games_genres = db.t.games_genres
    gameids = []
    gameids = games_genres(where=f"genre='{genre}'")
    games = db.t.games
    res = []
    for game in gameids:
        try:
            res.append(get_game(game["game"]))
        except NotFoundError:
            pass
    return res

def create_game(name: str, publisher: int, developer: int, release_date: str, genres: list|None = None, score: int|None = None, length: float|None = None, has_multiplayer: bool|None = None):
    db = database("../video_igre.db3")
    games = db.t.games
    res = games.insert(name=name, publisher=publisher, developer=developer, release_date=release_date, score=score, length=length, has_multiplayer=has_multiplayer)
    if genres:
        db.t.games_genres
        for genre in genres:
            db.execute("INSERT INTO games_genres (game, genre) VALUES (?, ?)", [res["id"], genre])
    return res["id"]

def update_game(id: int, name: str|None = None, publisher: int|None = None, developer: int|None = None, release_date: str|None = None, genres: list|None = None, score: int|None = None, length: float|None = None, has_multiplayer: bool|None = None):
    db = database("../video_igre.db3")
    games = db.t.games
    try:
        game = games[id]
    except NotFoundError:
        return None
    
    if name is not None:
        game["name"] = name
    if publisher is not None:
        game["publisher"] = publisher
    if developer is not None:
        game["developer"] = developer
    if release_date is not None:
        game["release_date"] = release_date
    if score is not None:
        game["score"] = score
    if length is not None:
        game["length"] = length
    if has_multiplayer is not None:
        game["has_multiplayer"] = has_multiplayer
    if name or publisher or developer or release_date or score or length or has_multiplayer:
        games.update(game)
    if genres is not None:
        db.execute("DELETE FROM games_genres WHERE game = ?", [id])
        for genre in genres:
            db.execute("INSERT INTO games_genres (game, genre) VALUES (?, ?)", [id, genre])

    return True

def delete_game(id: int):
    db = database("../video_igre.db3")
    games = db.t.games
    try:
        games[id]
        db.execute("DELETE FROM games_genres WHERE game = ?", [id])
        games.delete(id)
        return True
    except NotFoundError:
        return None

def get_company(id: int):
    db = database("../video_igre.db3")
    companies = db.t.companies
    try:
        res = companies[id]
        return res
    except NotFoundError:
        return None

def create_company(name: str, country_code: str|None, parent: int|None):
    db = database("../video_igre.db3")
    companies = db.t.companies
    res = companies.insert(name=name, country_code=country_code, parent=parent)
    return res["id"]

def update_company(id: int, name: str|None, country_code: str|None, parent: int|None):
    db = database("../video_igre.db3")
    companies = db.t.companies
    try:
        company = companies[id]
    except NotFoundError:
        return None
    print(company)
    if name:
        company["name"] = name
    if country_code:
        company["country_code"] = country_code
    if parent:
        company["parent"] = parent
    if name or country_code or parent:
        companies.update(company)
    print(company)
    return True

def delete_company(id: int):
    db = database("../video_igre.db3")
    companies = db.t.companies
    try:
        companies[id]
        companies.delete(id)
        return True
    except NotFoundError:
        return None
    
def get_genre(id: str):
    db = database("../video_igre.db3")
    genres = db.t.genres
    try:
        res = genres[id]
        return res
    except NotFoundError:
        return None

def create_genre(name: str, readable_name: str|None, parent: str|None):
    db = database("../video_igre.db3")
    genres = db.t.genres
    res = genres.insert(name=name, readable_name=readable_name, parent=parent)
    return res["name"]

def update_genre(name: str, readable_name: str|None, parent: str|None):
    db = database("../video_igre.db3")
    genres = db.t.genres
    try:
        genre = genres[name]
    except NotFoundError:
        return None
    print(genre)
    if name:
        genre["name"] = name
    if readable_name:
        genre["readable_name"] = readable_name
    if parent:
        genre["parent"] = parent
    if name or readable_name or parent:
        genres.update(genre)
    print(genre)
    return True

def delete_genre(id: str):
    db = database("../video_igre.db3")
    genres = db.t.genres
    try:
        genres[id]
        genres.delete(id)
        return True
    except NotFoundError:
        return None