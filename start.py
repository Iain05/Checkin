import click
import os
import csv
from datetime import datetime

today = datetime.today()
date_int = today.timetuple().tm_yday
mood_value = 6

@click.command()
def start() -> None:
    clear()
    mood_prompt()
    write_data()
    click.echo("Data stashed")

def mood_prompt() -> None:
    click.echo("How are you feeling today?")
    click.echo(click.style("0) in the trenches", fg="bright_black")
                + click.style(" 1) depressed", fg="bright_red")
                + click.style(" 2) sad", fg="yellow")
                + click.style(" 3) pretty meh", fg="green")
                + click.style(" 4) good", fg="cyan")
                + click.style(" 5) fantastic", fg="blue"))
    input = click.prompt(">", type=int)
    if input < 0 or input > 5:
        click.clear()
        click.echo("Please enter a value between 0 and 5.")
        mood_prompt()
    else:
        global mood_value
        mood_value = input
        return

# Clear the terminal and print some info at the top, just for a nicer UX
def clear() -> None:
    click.clear()
    click.echo(click.style("Checkin for " + today.strftime("%B {S}, %Y").replace("{S}", str(today.day)), underline=True))

""" Write the data to the CSV file
:requires: The data directory to exist and that the CSV file is properly formmatted
:modifies: The CSV file for the current year
Lots of things break this thing, zero promises are made about its functionality if the CSV is tampered with.
We only ever kee one copy of a day's data, so if you check in multiple times in a day, only the last one will be saved
"""
def write_data() -> None:
    written = False
    # TODO if the file doesn't exist, create it
    target_path = os.path.join(os.path.dirname(__file__), ("data/{Y}.csv").replace("{Y}", str(today.year)))

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
                writer.writerow([date_int, mood_value])
                written = True
            # If the date is greater than the current date, we insert the new data before it
            elif int(line[0]) > date_int and not written:
                writer.writerow([date_int, mood_value])
                writer.writerow(line)
                written = True
            # Otherwise, we just write the line back to the file
            else:
                writer.writerow(line)
        # If we never wrote the data, we write it at the end of the file
        if not written:
            writer.writerow([date_int, mood_value])