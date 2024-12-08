import click
import start
import graph
import spotify


@click.group()
def main() -> None:
    print("Hello, world!")


main.add_command(start.start)
main.add_command(graph.graph)
main.add_command(spotify.spotify)