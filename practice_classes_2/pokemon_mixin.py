class EmojiMixin:
    def __init__(self):
        original_str = self.__class__.__str__

        def new_str(self):
            text = original_str(self)
            for type, emoji in {'grass': '🌿', 'fire': '🔥', 'water': '🌊',
                                'electric': '⚡'}.items():
                text = text.replace(type, emoji)
            return text

        self.__class__.__str__ = new_str


class Pokemon(EmojiMixin):
    def __init__(self, name: str, category: str):
        super().__init__()
        self.name = name
        self.category = category

    def __str__(self):
        return f'{self.name}/{self.category}'


if __name__ == "__main__":
    pikachu = Pokemon(name='Pikachu', category='electric')
    print(pikachu)
    # Out: 'Pikachu/⚡'
