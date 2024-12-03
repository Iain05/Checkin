import click
import start

@click.group()
def main() -> None:
    print("Hello, world!")


main.add_command(start.start)
