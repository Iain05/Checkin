import click
from checkin import start
from checkin import graph
from checkin import spotify
from checkin import edit


@click.group()
def main() -> None:
    return


main.add_command(start.start)
main.add_command(graph.graph)
main.add_command(spotify.spotify)
main.add_command(edit.edit)
