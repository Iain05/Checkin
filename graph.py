import click
import os
import pandas as pd
from uniplot import plot
import plotext as plt
from colorscheme import COLORS


@click.command()
def graph() -> None:
    data = loadCSV(2024, "mood")
    energy_data = loadCSV(2024, "energy")
    data = data.rename(columns={"day": "mood of the day"})
    plt.plot(data.mood, color=COLORS.red.rgb)
    plt.plot(energy_data.energy)
    plt.yticks([0, 1, 2, 3, 4, 5], ["in the trenches", "depressed", "sad", "pretty meh", "good", "fantastic"])
    # TODO switch to using a day month format and display by the month
    plt.title("Mood of the day")
    plt.theme("pro")
    plt.show()
    # plot(xs=data.date, ys=data.mood, 
    #         lines=True,
    #         character_set="block",
    #         color=True,
    #         legend_labels=["mood"],
    #         y_gridlines=[0, 1, 2, 3, 4, 5],
    #     )


def loadCSV(year, metric) -> None:
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{year}.csv"))
    headers = ["date", "mood", "energy", "ate", "tv", "hobbies", "games"]
    return pd.read_csv(target_path, sep=',', names=headers, usecols=["date", metric])
