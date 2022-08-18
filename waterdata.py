#!/usr/bin/env python3

import csv
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import requests

sites = {
    "amistad": {
        "url": "https://www.ibwc.gov/wad/450800_a.txt",
        "fields": [
            "date",
            "time|cst",
            "elevation|meters",
            "storage|tcm",
            "surface area|ha",
        ],
        "models": [
            {"x": "date", "y": "storage|tcm", "pos": [0, 0]},
            {"x": "date", "y": "surface area|ha", "pos": [0, 1]},
        ],
    },
    "sanfelipe": {
        "url": "https://www.ibwc.gov/wad/453000_a.txt",
        "fields": [
            "date",
            "time|cst",
            "stage|meters",
            "discharge|cms",
            "preciptation|amm",
        ],
        "models": [
            {"x": "date", "y": "discharge|cms", "pos": [1, 0]},
            {"x": "date", "y": "preciptation|amm", "pos": [1, 1]},
        ],
    },
    "pecos": {
        "url": "https://www.ibwc.gov/wad/447410_a.txt",
        "fields": [
            "date",
            "time|cst",
            "stage|meters",
            "discharge|cms",
            "preciptation|amm",
        ],
        "models": [
            {"x": "date", "y": "discharge|cms", "pos": [2, 0]},
            {"x": "date", "y": "preciptation|amm", "pos": [2, 1]},
        ],
    },
}
cols = 2
rows = len(sites.keys())


def get_data(url: str) -> str:
    """Fetch the water data from the water data site."""
    req = requests.get(url)
    req.raise_for_status()
    return req.text


def structured_text_to_csv(text: str) -> List[list]:
    """Convert Water Data Text to CSV format."""
    data = text.splitlines()[4:]
    return [line.replace(",", "").split() for line in data]


def create_csv(data: List[list], filename: str, fields: list) -> None:
    """Create CSV file from water data."""
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerow(fields)
        writer.writerows(data)


if __name__ == "__main__":
    fig, axes = plt.subplots(nrows=rows, ncols=cols)

    for site, data in sites.items():
        url_data = get_data(data.get("url"))
        csv_data = structured_text_to_csv(url_data)
        create_csv(csv_data, f"{site}.csv", data.get("fields"))
        site_pd = pd.read_csv(f"{site}.csv")

        for model in data.get("models"):
            pos = model.get("pos")
            site_pd.plot(
                x=model.get("x"),
                y=model.get("y"),
                ax=axes[pos[0], pos[1]],
                title=f"{site.lower()} - {model.get('y').lower()}",
            )

    plt.show()
