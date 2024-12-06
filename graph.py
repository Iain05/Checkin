import click
import os
import pandas as pd
import plotext as plt
from colorscheme import COLORS


@click.command()
def graph() -> None:
    data = loadCSV(2024, "mood")
    energy_data = loadCSV(2024, "energy")
    data = data.rename(columns={"day": "mood of the day"})
    plt.plot(data.mood, color=COLORS.red.rgb, marker="braille")
    plt.plot(energy_data.energy, marker="braille")
    plt.yticks([0, 1, 2, 3, 4, 5], ["in the trenches", "depressed",
               "sad", "pretty meh", "good", "fantastic"])
    # TODO switch to using a day month format and display by the month
    plt.plot_size(min(plt.terminal_width(), 100),
                  min(plt.terminal_height(), 20))
    plt.title("Mood of the day")
    plt.theme("pro")
    plt.show()


def loadCSV(year, metric):
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{year}.csv"))
    headers = ["date", "mood", "energy", "ate", "tv", "hobbies", "games"]
    return pd.read_csv(filepath_or_buffer=target_path, sep=',', names=headers, usecols=["date", metric])
