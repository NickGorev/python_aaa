import json
from keyword import iskeyword


class FromJson:
    """Объект из JSON"""

    def __init__(self, json_dict: dict):
        for key, value in json_dict.items():
            while iskeyword(key):
                key += '_'

            if isinstance(value, dict):
                setattr(self, key, FromJson(value))
            elif isinstance(value, list):
                setattr(self, key, self._parse_list(value))
            else:
                setattr(self, key, value)

    def _parse_list(self, arr: list):
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
    """Изменяет цвет вывода в консоль метода __repr__"""

    color_changed = False

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not ColorizeMixin.color_changed:
            initial_repr: callable = getattr(self.__class__, "__repr__")

            def new_repr(self):
                color_escape = "\033[1;" + str(self.repr_color_code) + ";40m"
                drop_color = "\033[1;0;40m"
                return color_escape + initial_repr(self) + drop_color

            setattr(self.__class__, "__repr__", new_repr)

            ColorizeMixin.color_changed = True


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

    # выводит ĸатегорию при обращении через точĸу: corgi.class
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
