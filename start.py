import click
import os
import csv
import questionary
from datetime import datetime
from questionary import Style
from questionary import Choice


today = datetime.today()
date_int = today.timetuple().tm_yday
mood = -1
energy = -1

mood_energy_levels = {0: ["in the trenches", "giving up", "bright_black"], 
                        1: ["depressed", "exhausted", "red"],
                        2: ["sad", "tired", "yellow"],
                        3: ["pretty meh", "okay", "green"],
                        4: ["good", "good", "cyan"],
                        5: ["fantastic", "very high", "blue"]}

moods = [Choice(title = [("class:black", "0 | in the trenches")], value = 0),
         Choice(title = [("class:red", "1 | depressed")], value = 1),
         Choice(title = [("class:yellow", "2 | sad")], value = 2),
         Choice(title = [("class:green", "3 | pretty meh")], value = 3),
         Choice(title = [("class:cyan", "4 | good")], value = 4),
         Choice(title = [("class:blue", "5 | fantastic")], value = 5)]

energies = [Choice(title = [("class:black", "0 | giving up")], value = 0),
            Choice(title = [("class:red", "1 | exhausted")], value = 1),
            Choice(title = [("class:yellow", "2 | tired")], value = 2),
            Choice(title = [("class:green", "3 | okay")], value = 3),
            Choice(title = [("class:cyan", "4 | good")], value = 4),
            Choice(title = [("class:blue", "5 | very high")], value = 5)]

colored_items = questionary.Style([
    ("black", "fg:#45475a"),
    ("red", "fg:#f38ba8"),
    ("yellow", "fg:#f9e2af"),
    ("green", "fg:#a6e3a1"),
    ("cyan", "fg:#94e2d5"),
    ("blue", "fg:#89b4fa")
])

@click.command()
def start() -> None:
    clear()
    mood_selector()
    energy_selector()
    write_data_prompt()
    click.echo("Data stashed")

def mood_selector() -> None:
    input = questionary.select(
        "How are you feeling today?",
        choices=moods,
        use_arrow_keys=True,
        use_jk_keys=True,
        default=3,
        qmark="",
        instruction=[''],
        style=colored_items
    ).ask()
    global mood
    mood = input
    clear()
    return


def energy_selector() -> None:
    input = questionary.select(
        "How's your energy today?",
        choices=energies,
        use_arrow_keys=True,
        use_jk_keys=True,
        default=3,
        qmark="",
        instruction=[''],
        style=colored_items
    ).ask()
    global energy
    energy = input
    clear()
    return

def write_data_prompt() -> None:
    input = questionary.confirm("Save this Checkin?", auto_enter=False, qmark="").ask()
    if input:
        write_data()
    return

# Clear the terminal and print some info at the top, just for a nicer UX
def clear() -> None:
    click.clear()
    click.echo(click.style("Checkin for " + today.strftime("%B {S}, %Y").replace("{S}", str(today.day)), underline=True))
    data = [date_int, mood, energy]
    if (mood != -1):
        click.echo(click.style(" How are you feeling today?", bold=True))
        click.echo("    " + click.style(mood_energy_levels[mood][0], fg=mood_energy_levels[mood][2]))
    if (energy != -1):
        click.echo(click.style(" How's your energy today?", bold=True))
        click.echo("    " + click.style(mood_energy_levels[energy][1], fg=mood_energy_levels[energy][2]))

""" Write the data to the CSV file
:requires: The data directory to exist and that the CSV file is properly formmatted
:modifies: The CSV file for the current year
Lots of things break this thing, zero promises are made about its functionality if the CSV is tampered with.
We only ever kee one copy of a day's data, so if you check in multiple times in a day, only the last one will be saved
"""
def write_data() -> None:
    data = [date_int, mood, energy]
    written = False
    target_path = os.path.join(os.path.dirname(__file__), (f"data/{today.year}.csv"))

    # This creates the file if it doesnt exist
    with open(target_path, 'a', newline='') as file:
        file.close()

    # First we open a reader to read the existing data
    with open(target_path) as inf:
        reader = csv.reader(inf.readlines())

    # Once we have a reader, we can open the file again in write mode, the newline='' is to prevent extra newlines
    with open(target_path, 'w', newline='') as file:
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
