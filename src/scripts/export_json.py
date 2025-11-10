import json

from .db import get_data

def export_json():
    data = get_data()
    with open("../video_igre.json", "w", encoding="UTF-8", newline="\n") as file:
        file.write(json.dumps(data, indent=2, ))

if __name__ == "__main__":
    export_json()