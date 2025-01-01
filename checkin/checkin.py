import click
import start
import graph
import spotify
import edit


@click.group()
def main() -> None:
    return


main.add_command(start.start)
main.add_command(graph.graph)
main.add_command(spotify.spotify)
main.add_command(edit.edit)