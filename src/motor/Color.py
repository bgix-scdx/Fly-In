from enum import Enum
from typing import Tuple


class Color():
    R: int = 255
    G: int = 255
    B: int = 255

    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        '''Create a new RGB color'''
        self.R = r if r <= 255 else 255
        self.G = g if g <= 255 else 255
        self.B = b if b <= 255 else 255

    def __int__(self) -> int:
        '''Return the exadecimal value of the color.'''
        color = 0
        color = color | (self.R << 16)
        color = color | (self.G << 8)
        color = color | (self.B << 0)
        return (color)

    def __mul__(self, scalar: float) -> "Color":
        '''Return a new color with all color multipled by the scalar.'''
        return Color(
            round(self.R * scalar + 1),
            round(self.G * scalar + 1),
            round(self.B * scalar + 1),
        )

    def __rmul__(self, val: float | int) -> "Color":
        '''Return a new color with all color multipled by the scalar.'''
        return self.__mul__(val)

    def __add__(self, other: "Color") -> "Color":
        '''Return a new color with all color increased by the scalar.'''
        if not isinstance(other, Color):
            other = Color(other, other, other)
        return Color(self.R + other.R, self.G + other.G, self.B + other.B)

    def __sub__(self, other: "Color") -> "Color":
        '''Return a new color with all color decreased by the scalar.'''
        if not isinstance(other, Color):
            other = Color(other, other, other)
        return Color(self.R - other.R, self.G - other.G, self.B - other.B)

    def __radd__(self, other: "Color") -> "Color":
        '''Return a new color with all color increased by the scalar.'''
        return self.__add__(other)

    def __str__(self) -> str:
        '''Return the RGB as a string for display'''
        return f"({self.R}, {self.G}, {self.B})"

    def rgb(self) -> Tuple[int, int, int]:
        '''Return a tuple (R, G, B).'''
        return (self.R, self.G, self.B)


class ColorPallet(Enum):
    '''a set of named colors'''
    gold = Color(205, 255, 0)
    darkred = Color(200, 0, 0)
    maroon = Color(125, 125, 0)
    crimson = Color(255, 0, 0)
    black = Color(50, 50, 50)
    orange = Color(255, 155, 0)
    blue = Color(0, 0, 255)
    yellow = Color(155, 255, 0)
    brown = Color(125, 0, 0)
    purple = Color(200, 0, 255)
    green = Color(0, 200, 0)
    red = Color(200, 0, 0)
    violet = Color(200, 0, 100)
    rainbow = Color(256, 256, 256)
    lime = Color(125, 255, 0)
    cyan = Color(0, 255, 255)
    magenta = Color(255, 125, 0)
    lightbrown = Color(255, 255, 125)
    lightblue = Color(125, 125, 255)
    teal = Color(125, 255, 255)
    beige = Color(255, 255, 125)
