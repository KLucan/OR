import json
import tempfile

from fasthtml.common import *
from db import *
from errors import *
from scripts.export_json import export_json
from scripts.export_csv import export_csv
from scripts.db import get_data

exception_handlers = {500: internal_error}

app = FastHTML(exception_handlers=exception_handlers)


@app.route("/", methods="get")
def home():
    return FileResponse("../index.html")


@app.route("/datatable", methods="get")
def home():
    return FileResponse("../datatable.html")


@app.route("/video_igre.csv", methods="get")
def get():
    return FileResponse("../video_igre.csv", filename="video_igre.csv")


@app.route("/api/json", methods="get")
def get():
    with open("../video_igre.json", "r") as file:
        return JSONResponse(get_data())


@app.route("/get_csv", methods="get")
def get(search: str = "", vrijednost: str = ""):
    data = get_data(flat=True)
    res = []
    for row in data:
        if search:
            wholerow = ""
            if vrijednost:
                wholerow = str(row[vrijednost]).lower()
            else:
                for value in row.values():
                    if value:
                        wholerow += str(value).lower()
            if search.lower() not in wholerow:
                continue
        res.append(",".join([str(x) if x is not None else "" for x in row.values()]))
    return HTMLResponse("\n".join(res))


@app.route("/get_json", methods="get")
def get(search: str = "", vrijednost: str = ""):
    data = get_data(flat=True)
    res = []
    res_row = {}
    for row in data:
        if search:
            wholerow = ""
            if vrijednost:
                wholerow = str(row[vrijednost]).lower()
            else:
                for value in row.values():
                    if value:
                        wholerow += str(value).lower()
            if search.lower() not in wholerow:
                continue
        res.append(
            {
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
        )
    return JSONResponse(res)


@app.route("/api/html", methods="get", body_wrap=False)
def get(search: str = "", vrijednost: str = ""):
    data = get_data(flat=True)
    rows = []
    for row in data:
        if search:
            wholerow = ""
            if vrijednost:
                wholerow = str(row[vrijednost]).lower()
            else:
                for value in row.values():
                    if value:
                        wholerow += str(value).lower()
            if search.lower() not in wholerow:
                continue
        rows.append(
            Tr(
                Td(row["name"]),
                Td(row["publisher-name"]),
                Td(row["publisher-country-code"]),
                Td(row["developer-name"]),
                Td(row["developer-country-code"]),
                Td(row["release-date"]),
                Td(row["genres"]),
                Td(row["score"]),
                Td(row["length"]),
                Td(str(bool(row["has_multiplayer"]))),
            )
        )
    return Table(
        Thead(
            Tr(
                Th("Name"),
                Th("Publisher"),
                Th("Publisher country"),
                Th("Developer"),
                Th("Developer country"),
                Th("Release date"),
                Th("Genres"),
                Th("OpenCritic score"),
                Th("HLTB length"),
                Th("Has multiplayer?"),
            )
        ),
        Tbody(*rows),
    )


@app.route("/video_igre.json", methods="get")
def get():
    return FileResponse("../video_igre.json", filename="video_igre.json")


@app.route("/update_csv", methods=["post", "put"])
def post_or_put():
    export_csv()
    return "Refresh"


@app.route("/update_json", methods=["post", "put"])
def post_or_put():
    export_json()
    return "Refresh"

@app.route("/api/dump", methods="get")
def get():
    res = dump()
    return JSONResponse(
        {"status": "OK", "message": "Uspješno dohvaćena kolekcija igara.", "response": res},
        200,
    )

@app.route("/api/game/genre/{name}", methods="get")
def get(name: str):
    res = []
    try:
        res = get_game_genre(name)
    except NotFoundError:
        return not_found_error("Žanr s navedenim nazivom nije pronađen.")
    return JSONResponse(
        {"status": "OK", "message": "Uspješno dohvaćene igre za navedeni žanr.", "response": res},
        200,
    )

@app.route("/api/game", methods="post")
async def post(request):
    try:
        body = await request.body()
        data = json.loads(body.decode('utf-8'))
    except:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    name = data.get('name')
    publisher = data.get('publisher')
    developer = data.get('developer')
    release_date = data.get('release_date')
    genres = data.get('genres')
    score = data.get('score')
    length = data.get('length')
    has_multiplayer = data.get('has_multiplayer')
    if not name or not publisher or not developer or not release_date:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    if len(name) > 60:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    if get_company(publisher) is None or get_company(developer) is None:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    if length == "" or length == 0:
        length = None
    if score == "" or score == 0:
        score = None
    res = create_game(
        name, publisher, developer, release_date, genres, score, length, has_multiplayer
    )
    return JSONResponse(
        {"status": "OK", "message": "Igra uspješno kreirana.", "response": {"id": res}},
        201,
    )


@app.route("/api/game/{id}", methods="get")
def get(id: int):
    game = get_game(id)
    if game is None:
        return not_found_error("Igra s navedenim ID-om nije pronađena.")
    return JSONResponse(
        {"status": "OK", "message": "Uspješno dohvaćena igra.", "response": game}
    )


@app.route("/api/game/{id}", methods="put")
async def put(
    id: int,
    request
):
    try:
        body = await request.body()
        data = json.loads(body.decode('utf-8'))
    except:
        return bad_request_error("Neispravni podaci u zahtjevu.1")
    name = data.get('name')
    publisher = data.get('publisher')
    developer = data.get('developer')
    release_date = data.get('release_date')
    genres = data.get('genres')
    score = data.get('score')
    length = data.get('length')
    has_multiplayer = data.get('has_multiplayer')
    if id is None:
        return bad_request_error("Neispravni podaci u zahtjevu.3")
    if name is not None and len(name) > 60:
        return bad_request_error("Neispravni podaci u zahtjevu.2")
    if publisher is not None and get_company(publisher) is None or developer is not None and get_company(developer) is None:
        return bad_request_error("Neispravni podaci u zahtjevu.3")
    if length == "" or length == 0:
        length = None
    if score == "" or score == 0:
        score = None
    res = update_game(
        id, name, publisher, developer, release_date, genres, score, length, has_multiplayer
    )
    return JSONResponse(
        {"status": "OK", "message": "Igra uspješno ažurirana.", "response": {"id": res}},
        201,
    )


@app.route("/api/game/{id}", methods="delete")
def delete(id: int):
    game = delete_game(id)
    if game is None:
        return not_found_error("Igra s navedenim ID-om nije pronađena.")
    return JSONResponse(
        {"status": "OK", "message": "Igra uspješno izbrisana.", "response": None}
    )


@app.route("/api/company", methods="post")
def post(name: str = None, country_code: str | None = None, parent: int | None = None):
    if (
        len(name) > 60
        or len(country_code) > 2
        or parent is not None
        and get_company(parent) is None
    ):
        return bad_request_error("Neispravni podaci u zahtjevu.")
    res = create_company(name, country_code, parent)
    return JSONResponse(
        {
            "status": "OK",
            "message": "Kompanija uspješno kreirana.",
            "response": {"id": res},
        },
        201,
    )


@app.route("/api/company/{id}", methods="get")
def get(id: int):
    company = get_company(id)
    if company is None:
        return not_found_error("Kompanija s navedenim ID-om nije pronađena.")
    return JSONResponse(
        {
            "status": "OK",
            "message": "Uspješno dohvaćena kompanija.",
            "response": company,
        }
    )


@app.route("/api/company/{id}", methods="put")
def put(
    id: int,
    name: str | None = None,
    country_code: str | None = None,
    parent: int | None = None,
):
    if not name and not country_code and not parent:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    if (
        name is not None
        and len(name) > 60
        or country_code is not None
        and len(country_code) > 2
        or parent is not None
        and get_company(parent) is None
    ):
        return bad_request_error("Neispravni podaci u zahtjevu.")
    res = update_company(id, name, country_code, parent)
    if res is None:
        return not_found_error("Kompanija s navedenim ID-om nije pronađena.")
    return JSONResponse(
        {"status": "OK", "message": "Kompanija uspješno ažurirana.", "response": None}
    )


@app.route("/api/company/{id}", methods="delete")
def delete(id: int):
    company = delete_company(id)
    if company is None:
        return not_found_error("Kompanija s navedenim ID-om nije pronađena.")
    return JSONResponse(
        {"status": "OK", "message": "Kompanija uspješno izbrisana.", "response": None}
    )


@app.route("/api/genre", methods="post")
def post(name: str, readable_name: str | None = None, parent: str | None = None):
    if (
        len(name) > 20
        or len(readable_name) > 60
        or parent is not None
        and get_genre(parent) is None
    ):
        return bad_request_error("Neispravni podaci u zahtjevu.")
    res = create_genre(name, readable_name, parent)
    return JSONResponse(
        {"status": "OK", "message": "Žanr uspješno kreiran.", "response": {"id": res}},
        201,
    )


@app.route("/api/genre/{id}", methods="get")
def get(id: str):
    genre = get_genre(id)
    if genre is None:
        return not_found_error("Žanr s navedenim nazivom nije pronađen.")
    return JSONResponse(
        {"status": "OK", "message": "Uspješno dohvaćen žanr.", "response": genre}
    )


@app.route("/api/genre/{id}", methods="put")
def put(name: str, readable_name: str | None = None, parent: str | None = None):
    if not name and not readable_name and not parent:
        return bad_request_error("Neispravni podaci u zahtjevu.")
    if (
        name is not None
        and len(name) > 20
        or readable_name is not None
        and len(readable_name) > 60
        or parent is not None
        and get_genre(parent) is None
    ):
        return bad_request_error("Neispravni podaci u zahtjevu.")
    res = update_genre(name, readable_name, parent)
    if res is None:
        return not_found_error("Žanr s navedenim nazivom nije pronađen.")
    return JSONResponse(
        {"status": "OK", "message": "Žanr uspješno ažuriran.", "response": None}
    )


@app.route("/api/genre/{id}", methods="delete")
def delete(id: str):
    company = delete_genre(id)
    if company is None:
        return not_found_error("Žanr s navedenim nazivom nije pronađen.")
    return JSONResponse(
        {"status": "OK", "message": "Žanr uspješno izbrisan.", "response": None}
    )


@app.route("/api/openapi", methods="get")
def get():
    return FileResponse("../openapi.json")


serve()
