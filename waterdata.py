#!/usr/bin/env python3

import csv
from pprint import pprint
from typing import List

import matplotlib.pyplot as plt
import pandas as pd
import requests


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
    amistad = get_data("https://www.ibwc.gov/wad/450800_a.txt")
    sanfelipe = get_data("https://www.ibwc.gov/wad/453000_a.txt")
    amistad_data = structured_text_to_csv(amistad)
    sanfelipe_data = structured_text_to_csv(sanfelipe)
    create_csv(
        amistad_data,
        "amistad.csv",
        [
            "Date",
            "Time|CST",
            "Elevation|Meters",
            "Storage|Thousand Cubic Meters",
            "Surface Area|Hundred Acres",
        ],
    )
    create_csv(
        sanfelipe_data,
        "sanfelipe.csv",
        [
            "Date",
            "Time|CST",
            "Stage|Meters",
            "Discharge|Cubic Meters per Second",
            "Preciptation|Accumulation Milimeters",
        ],
    )
    amistad_pd = pd.read_csv("amistad.csv")
    sanfelipe_pd = pd.read_csv("sanfelipe.csv")
    fig, axes = plt.subplots(nrows=2, ncols=2)
    amistad_pd.plot(
        x="Date",
        y="Surface Area|Hundred Acres",
        ax=axes[0, 0],
        title="Lake Amistad | Surface Area",
    )
    amistad_pd.plot(
        x="Date",
        y="Storage|Thousand Cubic Meters",
        ax=axes[0, 1],
        title="Lake Amistad | Storage",
    )
    sanfelipe_pd.plot(
        x="Date",
        y="Discharge|Cubic Meters per Second",
        ax=axes[1, 0],
        title="San Felipe | Discharge",
    )
    sanfelipe_pd.plot(
        x="Date",
        y="Preciptation|Accumulation Milimeters",
        ax=axes[1, 1],
        title="San Felipe | Precipitation",
    )
    plt.show()
