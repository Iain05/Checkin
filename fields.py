import questionary
from questionary import Style, Choice
from catppuccin import PALETTE


def rgbToTuple(rgb):
    rgbTuple = [rgb.r, rgb.g, rgb.b]
    return rgbTuple


mood_energy_levels = {0: ["in the trenches", "giving up", rgbToTuple(PALETTE.mocha.colors.surface1.rgb)],
                      1: ["depressed", "exhausted", rgbToTuple(PALETTE.mocha.colors.red.rgb)],
                      2: ["sad", "tired", rgbToTuple(PALETTE.mocha.colors.yellow.rgb)],
                      3: ["pretty meh", "okay", rgbToTuple(PALETTE.mocha.colors.green.rgb)],
                      4: ["good", "good", rgbToTuple(PALETTE.mocha.colors.teal.rgb)],
                      5: ["fantastic", "very high", rgbToTuple(PALETTE.mocha.colors.blue.rgb)]}
moods = [Choice(title=[("class:black", "0 | in the trenches")], value=0),
         Choice(title=[("class:red", "1 | depressed")], value=1),
         Choice(title=[("class:yellow", "2 | sad")], value=2),
         Choice(title=[("class:green", "3 | pretty meh")], value=3),
         Choice(title=[("class:cyan", "4 | good")], value=4),
         Choice(title=[("class:blue", "5 | fantastic")], value=5)]
energies = [Choice(title=[("class:black", "0 | giving up")], value=0),
            Choice(title=[("class:red", "1 | exhausted")], value=1),
            Choice(title=[("class:yellow", "2 | tired")], value=2),
            Choice(title=[("class:green", "3 | okay")], value=3),
            Choice(title=[("class:cyan", "4 | good")], value=4),
            Choice(title=[("class:blue", "5 | very high")], value=5)]
activities = ("Went out to eat", "Watched TV or a movie",
              "Spent time on hobbies", "Played video games")

colored_items = questionary.Style([
    ("black", "fg:" + PALETTE.mocha.colors.surface1.hex),
    ("red", "fg:" + PALETTE.mocha.colors.red.hex),
    ("yellow", "fg:" + PALETTE.mocha.colors.yellow.hex),
    ("green", "fg:" + PALETTE.mocha.colors.green.hex),
    ("cyan", "fg:" + PALETTE.mocha.colors.teal.hex),
    ("blue", "fg:" + PALETTE.mocha.colors.blue.hex)
])
