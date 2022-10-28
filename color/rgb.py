from __future__ import annotations
from collections import namedtuple

RGB = namedtuple('RGB', ['red', 'green', 'blue'])


class Color:
    def __init__(self: Color, red: int, green: int, blue: int):
        self.rgb = RGB(red, green, blue)

    def __repr__(self: Color) -> str:
        """Генерирует жирную точку,
        которая выводится в консоль заданным цветом"""
        END = '\033[0'
        START = '\033[1;38;2'
        MOD = 'm'
        return f'{START};{self.rgb.red};{self.rgb.green};{self.rgb.blue}{MOD}'\
               f'●{END}{MOD}'

    def __eq__(self: Color, other: Color) -> bool:
        return self.rgb == other.rgb

    def __add__(self: Color, other: Color) -> Color:
        """Смешивает два цвета через сложение экземпляров класса"""
        red = min(self.rgb.red + other.rgb.red, 255)
        green = min(self.rgb.green + other.rgb.green, 255)
        blue = min(self.rgb.blue + other.rgb.blue, 255)
        return type(self)(red, green, blue)

    def __hash__(self: Color) -> int:
        return hash(self.rgb)

    def __mul__(self: Color, c: float) -> Color:
        """Уменьшение контраста"""
        cl = -256 * (1 - c)
        F = 259 * (cl + 255) / (255 * (259 - cl))

        def corr_color(color_component):
            return int(F * (color_component - 128) + 128)

        return type(self)(corr_color(self.rgb.red),
                          corr_color(self.rgb.green),
                          corr_color(self.rgb.blue))

    __rmul__ = __mul__


if __name__ == "__main__":
    print('Создание объекта Color красного цвета')
    red = Color(255, 0, 0)
    print(red)

    print('------------------------------------')
    print('Сравнение на равенство')
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    print(red, '==', green, f'=> {red == green}')
    # Out: False
    print(red, '==', Color(255, 0, 0), f'=> {red == Color(255, 0, 0)}')
    # Out: True

    print('------------------------------------')
    print('Сложение объектов')
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    print(red, '+', green, '=', red + green)

    print('------------------------------------')
    print('Из списка цветов оставьте только уникальные')
    print('Хеш и множество')
    orange1 = Color(255, 165, 0)
    red = Color(255, 0, 0)
    green = Color(0, 255, 0)
    orange2 = Color(255, 165, 0)
    color_list = [orange1, red, green, orange2]
    print('set([', orange1, red, green, orange2, ']) = ', set(color_list))

    print('------------------------------------')
    print('Уменьшение контраста')
    red = Color(255, 0, 0)
    print('0.5 *', red, ' = ', 0.5 * red)
    print(red, '* 0.7 = ', red * 0.7)
