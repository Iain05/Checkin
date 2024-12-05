from catppuccin import PALETTE

class Color:
    def __init__(self, rgb, hex_value):
        self.rgb = rgb
        self.hex = hex_value

class Colors:
    def __init__(self, palette):
        self.surface1 = Color(rgbToTuple(palette.mocha.colors.surface1.rgb), palette.mocha.colors.surface1.hex)
        self.red = Color(rgbToTuple(palette.mocha.colors.red.rgb), palette.mocha.colors.red.hex)
        self.yellow = Color(rgbToTuple(palette.mocha.colors.yellow.rgb), palette.mocha.colors.yellow.hex)
        self.green = Color(rgbToTuple(palette.mocha.colors.green.rgb), palette.mocha.colors.green.hex)
        self.teal = Color(rgbToTuple(palette.mocha.colors.teal.rgb), palette.mocha.colors.teal.hex)
        self.blue = Color(rgbToTuple(palette.mocha.colors.blue.rgb), palette.mocha.colors.blue.hex)

def rgbToTuple(rgb):
    return [rgb.r, rgb.g, rgb.b]

COLORS = Colors(PALETTE)
