import csv

from .db import get_data

def export_csv():
    data = get_data(flat=True)
    with open("../video_igre.csv", "w", encoding="UTF-8", newline="") as file:
        writer = csv.writer(file, delimiter=",", dialect="unix")
        for row in data:
            writer.writerow(row.values())

if __name__ == "__main__":
    export_csv()