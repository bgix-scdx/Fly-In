class Color():
    R: int = 255
    G: int = 255
    B: int = 255

    def __init__(self, r: int = 255, g: int = 255, b: int = 255):
        self.R = r if r <= 255 else 255
        self.G = g if g <= 255 else 255
        self.B = b if b <= 255 else 255

    def __int__(self) -> int:
        color = 0
        color = color | (self.R << 16)
        color = color | (self.G << 8)
        color = color | (self.B << 0)
        return (color)

    def __mul__(self, scalar: float) -> "Color":
        return Color(
            round(self.R * scalar + 1),
            round(self.G * scalar + 1),
            round(self.B * scalar + 1),
        )

    def __rmul__(self, val: float | int) -> "Color":
        return self.__mul__(val)

    def __add__(self, other: "Color") -> "Color":
        if not isinstance(other, Color):
            other = Color(other, other, other)
        return Color(self.R + other.R, self.G + other.G, self.B + other.B)

    def __sub__(self, other: "Color") -> "Color":
        if not isinstance(other, Color):
            other = Color(other, other, other)
        return Color(self.R - other.R, self.G - other.G, self.B - other.B)

    def __radd__(self, other) -> "Color":
        return self.__add__(other)

    def __str__(self) -> "Color":
        return f"({self.R}, {self.G}, {self.B})"
