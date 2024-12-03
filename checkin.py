import click
import start
import graph


@click.group()
def main() -> None:
    print("Hello, world!")


main.add_command(start.start)
main.add_command(graph.graph)
