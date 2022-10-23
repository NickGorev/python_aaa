from base_pokemon import BasePokemon


class Pokemon(BasePokemon):
    def __init__(self, name, category, weaknesses=None):
        super().__init__(name, category)
        self.weaknesses = weaknesses


if __name__ == "__main__":
    charmander = Pokemon(
        name='Charmander',
        category='Lizard',
        weaknesses=('water', 'ground', 'rock')
    )

    print(charmander.to_str())

    # Out: 'Charmander/Lizard'
