import click
import os
import csv
import questionary
import pandas as pd
from datetime import datetime, timedelta

from checkin.fields import *
from checkin.config import *

from checkin.spotify import store_month_data

today = datetime.today()
mood_answer = -1
energy_answer = -1
activities_answer = [False] * len(activities)
productive_answer = 0
sleep_answer = 0


state = 0


@click.command()
@click.argument(
    "checkin_day", type=click.DateTime(["%Y-%m-%d"]), default=datetime.today()
)
def start(checkin_day) -> None:
    """
    Args:
        checkin_day: The day to check in for.

    Main function to start the check-in process.
    Clears the terminal, prompts the user for mood, energy, and activities,
    then writes the data and checks Spotify data if applicable.
    """
    global today
    today = checkin_day
    if today.date() == datetime.today().date():
        missed_checkins = missed_dates()
        if missed_checkins != []:
            prompt_missing_dates(missed_checkins=missed_checkins)
            return
    clear()
    mood_selector()
    energy_selector()
    activities_selector()
    hours_prompt("How many hours were you productive today?", "productive")
    hours_prompt("How many hours did you sleep today?", "sleep")
    write_data_prompt()
    check_spotify()


@click.pass_context
def prompt_missing_dates(context, missed_checkins) -> None:
    clear()
    input = questionary.confirm(
        "You have some missed checkins, would you like to view/edit them?",
        auto_enter=False,
        qmark="",
        style=standard_style,
    ).ask()
    if input:
        context.invoke(start, checkin_day=missed_checkins[0])
    return


def check_spotify() -> None:
    """
    Prompts the user to select their mood for the day using a questionary select prompt.
    Updates the global mood_answer and state variables.
    """
    if datetime.today().day >= 20:
        store_month_data()


def mood_selector() -> None:
    """
    Prompts the user to select their mood for the day using a questionary select prompt.
    Updates the global mood_answer and state variables.
    """
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
    """
    Prompts the user to select their energy level for the day using a questionary select prompt.
    Updates the global energy_answer and state variables.
    """
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
    """
    Prompts the user to select their activities for the day using a questionary checkbox prompt.
    Updates the global activities_answer and state variables.
    """
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


def hours_prompt(prompt: str, type: str) -> None:
    """
    Prompt the user to input the hours they were productive for the day.
    """
    input = questionary.text(
        prompt,
        validate=HoursValidator(),
    ).ask()
    global state
    state += 1
    if type == "productive":
        global productive_answer
        productive_answer = input
    else:
        global sleep_answer
        sleep_answer = input
    clear()


def write_data_prompt() -> None:
    """
    Prompts the user to confirm if they want to save the check-in data.
    If confirmed, calls the write_data function and displays a success message.
    Otherwise, displays a discard message.
    """
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


def clear() -> None:
    """
    Clears the terminal and prints the current check-in state.
    Displays the date and the user's mood, energy, and activities based on the current state.
    """
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
    if state >= 4:
        click.echo(click.style(" How many hours were you productive today?", bold=True))
        click.echo(f"    {productive_answer}")
    if state >= 5:
        click.echo(click.style(" How many hours did you sleep today?", bold=True))
        click.echo(f"    {sleep_answer}")


def write_data() -> None:
    """Write the data to the CSV file

    Requires: The data directory to exist and that the CSV file is properly formmatted
    Modifies: The CSV file for the current year

    Lots of things break this thing, zero promises are made about its functionality if the CSV is tampered with.
    We only ever kee one copy of a day's data, so if you check in multiple times in a day, only the last one will be saved
    """
    data = [today.strftime("%Y-%m-%d"), mood_answer, energy_answer] + activities_answer
    data.append(productive_answer)
    data.append(sleep_answer)
    written = False
    target_path = os.path.join(DEFAULT_DIR, (f"data/{today.year}.csv"))

    # This creates the file if it doesnt exist
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
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
            if line[0] == today.strftime("%Y-%m-%d"):
                writer.writerow(data)
                written = True
            # If the date is greater than the current date, we insert the new data before it
            elif datetime.strptime(line[0], "%Y-%m-%d") > today and not written:
                writer.writerow(data)
                writer.writerow(line)
                written = True
            # Otherwise, we just write the line back to the file
            else:
                writer.writerow(line)
        # If we never wrote the data, we write it at the end of the file
        if not written:
            writer.writerow(data)


def missed_dates() -> list[datetime]:
    """
    Determines the dates that are missing from the CSV file for the current year.
    is not dependent on the global variable today, it always checks the current year.
    It determines missing dates by checking from the start of the csv file to the
    current date.
    Returns:
        A list of datetime objects representing the missing dates.
    """
    target_path = os.path.join(DEFAULT_DIR, (f"data/{today.year}.csv"))
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "a", newline="") as file:
        file.close()

    with open(target_path) as file:
        reader = csv.reader(file.readlines())
        try:
            start_date = next(reader)[0]
        except:
            return []
        dates = (
            pd.date_range(start=start_date, end=datetime.today() - timedelta(1))
            .to_pydatetime()
            .tolist()
        )
        try:
            dates.remove(datetime.strptime(start_date, "%Y-%m-%d"))
        except Exception as e:
            pass
        file.seek(0)
        print(start_date)
        for line in reader:
            try:
                dates.remove(datetime.strptime(line[0], "%Y-%m-%d"))
            except:
                pass
        return dates
