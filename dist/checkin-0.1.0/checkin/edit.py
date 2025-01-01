import click
import csv
from datetime import datetime
from start import start

from fields import moods, energies, activities, mood_energy_levels

@click.command()
@click.argument("date", type=click.DateTime(["%Y-%m-%d"]), required=False)
@click.option("-v", "--view", is_flag=True, help="View a checkin")
@click.option("-m", "--missed", is_flag=True, help="View missed checkins")
@click.pass_context
def edit(context, date, view, missed) -> None:
    """
    Command to edit or view a checkin.
    
    Args:
        context: Click context to invoke other commands.
        date: The date of the checkin to edit or view (format: %Y-%m-%d).
        view: Flag to view a checkin.
        missed: Flag to view missed checkins.
    """
    if date is not None and view:
        view_checkin(date)
    elif date is None and view:
        click.echo("Feature not implemented yet L")
    elif date is not None:
        context.invoke(start, checkin_day=date)
    else:
        context.invoke(start)

def find_line(date: datetime) -> list | None:
    """
    Finds the checkin data for a given date in the CSV file.
    
    Args:
        date: The date to find the checkin for.
    
    Returns:
        The checkin data as a list, or None if not found.
    """
    with open(f"data/{date.year}.csv") as file:
        reader = csv.reader(file.readlines())
        file.seek(0)
        for line in reader:
            if line[0] == date.strftime("%Y-%m-%d"):
                return line
        file.close()
    return None

def view_checkin(date: datetime) -> None:
    """
    Displays the checkin data for a given date.
    
    Args:
        date: The date of the checkin to view.
    """
    line = find_line(date)
    if line is None:
        click.echo("No checkin found for that date.")
        return
    click.echo(f"Checkin for {line[0]}")
    click.echo("Mood: ", nl=False)
    click.echo(click.style(mood_energy_levels[int(line[1])][0], fg=mood_energy_levels[int(line[1])][2]))
    click.echo("Energy: ", nl=False)
    click.echo(click.style(mood_energy_levels[int(line[2])][1], fg=mood_energy_levels[int(line[2])][2]))
    click.echo("Activities: ")
    for i, activity in enumerate(activities):
        if line[i + 3] == "True":
            click.echo(f" - {activity}")