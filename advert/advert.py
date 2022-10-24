import json
import functools
from typing import Callable
from keyword import iskeyword


class FromJson:
    """Объект из JSON"""

    def __init__(self, json_dict: dict):
        """
        Создане объекта из словаря JSON
        ключи словаря - названия атрибутов
            (в случае совпадения с ключевым словом, добавляется символ "_")
        значения словаря - значения атрибутов с возможной вложенностью JSON
        """
        for key, value in json_dict.items():
            if iskeyword(key):
                key += '_'

            if isinstance(value, dict):
                setattr(self, key, FromJson(value))
            elif isinstance(value, list):
                setattr(self, key, self._parse_list(value))
            else:
                setattr(self, key, value)

    def _parse_list(self, arr: list) -> list:
        """
        Обработка списка с учетом возможной вложенности структур JSON
        """
        ans = []
        for item in arr:
            if isinstance(item, list):
                ans.append(self._parse_list(item))
            elif isinstance(item, dict):
                ans.append(FromJson(item))
            else:
                ans.append(item)
        return ans


class ColorizeMixin:
    """
    Изменяет цвет вывода в консоль метода __repr__
    Подменяет функцию __repr__() у класса классе переменной self
    """

    def __init_subclass__(cls, *args, **kwargs):
        super().__init_subclass__(*args, **kwargs)
        cls.__repr__ = cls._replace_repr(cls.__repr__)

    @classmethod
    def _replace_repr(cls, func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            text: str = func(*args, **kwargs)
            color_escape = "\033[1;" + str(cls.repr_color_code) + ";40m"
            drop_color = "\033[1;0;40m"
            return color_escape + text + drop_color
        return wrapper


class Advert(ColorizeMixin, FromJson):
    """Объект рекламное объявление, создаваемый из JSON"""

    repr_color_code = 33  # yellow

    def __init__(self, json_dict: dict):
        super().__init__(json_dict)
        if not hasattr(self, "title"):
            raise ValueError("must have a title attribute")

        if hasattr(self, "price"):
            if self.price < 0:
                raise ValueError("price must be >= 0")
        else:
            self.price = 0

    def __repr__(self):
        return f"{self.title} | {self.price} ₽"


if __name__ == '__main__':
    # проверка атрибута title
    try:
        advert_0 = Advert(
            json.loads(
                """{
                }"""
            )
        )
    except ValueError as e:
        assert str(e) == "must have a title attribute"

    # атрибут title присутствует, атрибута price нет,
    # должен создаеться атрибут price со значением 0
    advert_1 = Advert(
        json.loads(
            """{
                "title": "test"
            }"""
        )
    )
    assert advert_1.title == "test"
    assert advert_1.price == 0

    # корректные атрибуты title, price
    advert_2 = Advert(
        json.loads(
            """{
                "title": "test",
                "price": 100
            }"""
        )
    )
    assert advert_1.title == "test"
    assert advert_2.price == 100

    # некорректный (отрицательный) атрибут price
    try:
        advert_3 = Advert(
            json.loads(
                """{
                    "title": "test",
                    "price": -100
                }"""
            )
        )
    except ValueError as e:
        assert str(e) == "price must be >= 0"

    # глубокая вложенность json
    advert_4 = Advert(
        json.loads(
            """{
                "title": "test",
                "attr_1": {
                    "attr_2": [
                        0, 1, 2, 3, 4,
                        {
                            "attr_3": "deep attribute"
                        }
                    ]
                }
            }"""
        )
    )
    assert advert_4.attr_1.attr_2[5].attr_3 == "deep attribute"

    # выводится адрес при обращении ĸ атрибуту через точĸи: ad.location.address
    advert_5 = Advert(
        json.loads(
            """{
                "title": "python",
                "price": 0,
                "location": {
                    "address": "город Москва, Лесная, 7",
                    "metro_stations": ["Белорусская"]
                }
            }"""
        )
    )
    assert advert_5.location.address == "город Москва, Лесная, 7"

    # выводит ĸатегорию при обращении через точĸу: corgi.class_
    corgi = Advert(
        json.loads(
            """{
                "title": "Вельш-корги",
                "price": 1000,
                "class": "dogs",
                "location": {
                    "address": "город Самара, улица Мориса Тореза, 50"
                }
            }"""
        )
    )
    assert corgi.class_ == "dogs"

    # при выводе обяъвления в ĸонсоли print(corgi) получаем надпись
    # 'Вельш-ĸорги | 1000 ₽' желтым цветом
    print(corgi)
