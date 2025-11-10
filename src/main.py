import json
import tempfile

from fasthtml.common import *
from scripts.export_json import export_json
from scripts.export_csv import export_csv
from scripts.db import get_data

app = FastHTML()


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


serve()
