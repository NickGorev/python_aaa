class BasePokemon:
    def __init__(self, name, category):
        self.name = name
        self.category = category

    def to_str(self):
        return f'{self.name}/{self.category}'


if __name__ == "__main__":
    base_charmander = BasePokemon(name='Charmander', category='Lizard')
    print(base_charmander.to_str())

    # Out: 'Charmander/Lizard'
