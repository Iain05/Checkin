import questionary
from questionary import Style, Choice
from colorscheme import COLORS

mood_energy_levels = {
    0: ["in the trenches", "giving up", COLORS.surface1.rgb],
    1: ["depressed", "exhausted", COLORS.red.rgb],
    2: ["sad", "tired", COLORS.yellow.rgb],
    3: ["pretty meh", "okay", COLORS.green.rgb],
    4: ["good", "good", COLORS.teal.rgb],
    5: ["fantastic", "very high", COLORS.blue.rgb]
}

moods = [
    Choice(title=[("class:black", "0 | in the trenches")], value=0),
    Choice(title=[("class:red", "1 | depressed")], value=1),
    Choice(title=[("class:yellow", "2 | sad")], value=2),
    Choice(title=[("class:green", "3 | pretty meh")], value=3),
    Choice(title=[("class:cyan", "4 | good")], value=4),
    Choice(title=[("class:blue", "5 | fantastic")], value=5)
]

energies = [
    Choice(title=[("class:black", "0 | giving up")], value=0),
    Choice(title=[("class:red", "1 | exhausted")], value=1),
    Choice(title=[("class:yellow", "2 | tired")], value=2),
    Choice(title=[("class:green", "3 | okay")], value=3),
    Choice(title=[("class:cyan", "4 | good")], value=4),
    Choice(title=[("class:blue", "5 | very high")], value=5)
]

activities = (
    "Went out to eat", "Watched TV or a movie",
    "Spent time on hobbies", "Played video games"
)

colored_items = questionary.Style([
    ("black", "fg:" + COLORS.surface1.hex),
    ("red", "fg:" + COLORS.red.hex),
    ("yellow", "fg:" + COLORS.yellow.hex),
    ("green", "fg:" + COLORS.green.hex),
    ("cyan", "fg:" + COLORS.teal.hex),
    ("blue", "fg:" + COLORS.blue.hex)
])

standard_style = questionary.Style([
    ("answer", "fg:" + COLORS.blue.hex)
])
