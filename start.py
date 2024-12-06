import click
import os
import csv
import questionary
from datetime import datetime

from fields import mood_energy_levels, colored_items
from fields import selector_style, standard_style
from fields import moods, energies, activities

today = datetime.today()
date_int = today.timetuple().tm_yday
mood_answer = -1
energy_answer = -1
activities_answer = [False, False, False, False]

state = 0


@click.command()
def start() -> None:
    clear()
    mood_selector()
    energy_selector()
    activities_selector()
    write_data_prompt()


def mood_selector() -> None:
    input = questionary.select(
        "How are you feeling today?",
        choices=moods,
        use_arrow_keys=True,
        use_jk_keys=True,
        qmark="",
        instruction="",
        style=colored_items,
    ).ask()
    global mood_answer, state
    mood_answer = input
    state += 1
    clear()
    return


def energy_selector() -> None:
    input = questionary.select(
        "How's your energy today?",
        choices=energies,
        use_arrow_keys=True,
        use_jk_keys=True,
        qmark="",
        instruction="",
        style=colored_items,
    ).ask()
    global energy_answer, state
    energy_answer = input
    state += 1
    clear()
    return


def activities_selector():
    input = questionary.checkbox(
        "What have you done or will you do today?",
        choices=activities,
        style=selector_style,
        instruction="(<space> to select)",
    ).ask()
    global activities_answer, state
    for e in input:
        activities_answer[activities.index(e)] = True
    state += 1
    click.echo(activities_answer)
    clear()
    return


def write_data_prompt() -> None:
    input = questionary.confirm(
        "Save this Checkin?", auto_enter=False, qmark="", style=standard_style
    ).ask()
    if input:
        write_data()
        click.echo(
            "Checkin for "
            + today.strftime("%B {S}, %Y").replace("{S}", str(today.day))
            + " saved!"
        )
    else:
        click.echo("Checkin discarded")
    return


# Clear the terminal and print some info at the top, just for a nicer UX


def clear() -> None:
    click.clear()
    click.echo(
        click.style(
            "Checkin for "
            + today.strftime("%B {S}, %Y").replace("{S}", str(today.day)),
            underline=True,
        )
    )
    if state >= 1:
        click.echo(click.style(" How are you feeling today?", bold=True))
        click.echo(
            "    "
            + click.style(
                mood_energy_levels[mood_answer][0],
                fg=mood_energy_levels[mood_answer][2],
            )
        )
    if state >= 2:
        click.echo(click.style(" How's your energy today?", bold=True))
        click.echo(
            "    "
            + click.style(
                mood_energy_levels[energy_answer][1],
                fg=mood_energy_levels[energy_answer][2],
            )
        )
    if state >= 3:
        click.echo(click.style(" What have you done or will you do today?", bold=True))
        for i, e in enumerate(activities_answer):
            click.echo("    " + click.style(activities[i], fg="blue")) if e else None


""" Write the data to the CSV file
:requires: The data directory to exist and that the CSV file is properly formmatted
:modifies: The CSV file for the current year
Lots of things break this thing, zero promises are made about its functionality if the CSV is tampered with.
We only ever kee one copy of a day's data, so if you check in multiple times in a day, only the last one will be saved
"""


def write_data() -> None:
    data = [date_int, mood_answer, energy_answer] + activities_answer
    written = False
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{today.year}.csv"))

    # This creates the file if it doesnt exist
    with open(target_path, "a", newline="") as file:
        file.close()

    # First we open a reader to read the existing data
    with open(target_path) as inf:
        reader = csv.reader(inf.readlines())

    # Once we have a reader, we can open the file again in write mode, the newline='' is to prevent extra newlines
    with open(target_path, "w", newline="") as file:
        file.seek(0)
        writer = csv.writer(file)
        for line in reader:
            # If the date is already in the file, we overwrite it
            if line[0] == str(date_int):
                writer.writerow(data)
                written = True
            # If the date is greater than the current date, we insert the new data before it
            elif int(line[0]) > date_int and not written:
                writer.writerow(data)
                writer.writerow(line)
                written = True
            # Otherwise, we just write the line back to the file
            else:
                writer.writerow(line)
        # If we never wrote the data, we write it at the end of the file
        if not written:
            writer.writerow(data)
