import click
import os
import pandas as pd
import plotext as plt
from checkin.colorscheme import COLORS
from checkin.config import *
from datetime import datetime


today = datetime.today()

plt.date_form("Y-m-d")


@click.command()
@click.option("-y", default=today.year, help="The year of data to graph")
def graph(y) -> None:
    data = loadCSV(y, "mood")
    energy_data = loadCSV(y, "energy")
    plt.plot(data.date, data.mood, color=COLORS.red.rgb, marker="braille")
    plt.plot(data.date, energy_data.energy, marker="braille")
    plt.yticks(
        [0, 1, 2, 3, 4, 5],
        ["in the trenches", "depressed", "sad", "pretty meh", "good", "fantastic"],
    )
    term_width = plt.terminal_width()
    term_height = plt.terminal_height()
    if term_width is not None and term_height is not None:
        plt.plot_size(min(term_width, 100), min(term_height, 20))
    plt.title("Mood of the day")
    plt.theme("pro")
    plt.show()


def loadCSV(year, metric):
    target_path = os.path.join(DEFAULT_DIR, (f"data/{year}.csv"))
    headers = [
        "date",
        "mood",
        "energy",
        "ate",
        "tv",
        "hobbies",
        "games",
        "cried",
        "productive",
        "sleep",
    ]
    return pd.read_csv(
        filepath_or_buffer=target_path, sep=",", names=headers, usecols=["date", metric]
    )
