import click
import os
import pandas as pd
from uniplot import plot


@click.command()
def graph() -> None:
    loadCSV(2024)


def loadCSV(year) -> None:
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{year}.csv"))
    headers = ["date", "mood", "energy", "ate", "tv", "hobbies", "games"]
    data = pd.read_csv(target_path, sep=',', names=headers,
                       usecols=["date", "mood"])
    data = data.rename(columns={"day": "mood of the day"})
    plot(xs=data.date, ys=data.mood, lines=True)
