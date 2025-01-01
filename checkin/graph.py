import click
import os
import pandas as pd
import plotext as plt
from colorscheme import COLORS

plt.date_form("Y-m-d")

@click.command()
def graph() -> None:
    data = loadCSV(2024, "mood")
    energy_data = loadCSV(2024, "energy")
    plt.plot(data.date, data.mood, color=COLORS.red.rgb, marker="braille")
    plt.plot(data.date, energy_data.energy, marker="braille")
    plt.yticks([0, 1, 2, 3, 4, 5], ["in the trenches", "depressed",
               "sad", "pretty meh", "good", "fantastic"])
    term_width = plt.terminal_width()
    term_height = plt.terminal_height()
    if term_width is not None and term_height is not None:
        plt.plot_size(min(term_width, 100),
                    min(term_height, 20))
    plt.title("Mood of the day")
    plt.theme("pro")
    plt.show()


def loadCSV(year, metric):
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{year}.csv"))
    headers = ["date", "mood", "energy", "ate", "tv", "hobbies", "games", "cried"]
    return pd.read_csv(filepath_or_buffer=target_path, sep=',', names=headers, usecols=["date", metric])
