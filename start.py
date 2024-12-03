import click
import os
import csv
from datetime import datetime

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

@click.command()
def start() -> None:
    clear()
    mood_prompt()
    energy_prompt()
    write_data()
    click.echo("Data stashed")

def mood_prompt() -> None:
    click.echo("How are you feeling today?")
    for (i, level) in mood_energy_levels.items():
        click.echo(click.style(str(i) + ") " + level[0] + "  ", fg=level[2]), nl=False)
    click.echo()
    input = click.prompt(">>>", type=int)
    if input < 0 or input > 5:
        click.clear()
        click.echo("Please enter a value between 0 and 5.")
        mood_prompt()
    else:
        global mood
        mood = input
        clear()
        return

def energy_prompt() -> None:
    click.echo("What's your energy level like?")
    for (i, level) in mood_energy_levels.items():
        click.echo(click.style(str(i) + ") " + level[1] + "  ", fg=level[2]), nl=False)
    click.echo()
    input = click.prompt(">>>", type=int)
    if input < 0 or input > 5:
        click.clear()
        click.echo("Please enter a value between 0 and 5.")
        energy_prompt()
    else:
        global energy
        energy = input
        clear()
        return
# Clear the terminal and print some info at the top, just for a nicer UX
def clear() -> None:
    click.clear()
    click.echo(click.style("Checkin for " + today.strftime("%B {S}, %Y").replace("{S}", str(today.day)), underline=True))
    data = [date_int, mood, energy]
    click.echo("---- Responses so far ----")
    click.echo("Mood: " + click.style(mood_energy_levels[mood][0], fg=mood_energy_levels[mood][2])) if mood != -1 else None



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