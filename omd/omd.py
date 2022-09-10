# Guido van Rossum <guido@python.org>

def step1():
    print(
        'Утка-маляр 🦆 решила выпить зайти в бар. '
        'Взять ей зонтик? ☂️'
    )
    option = ''
    options = {'да': True, 'нет': False}
    while option not in options:
        print('Выберите: {}/{}'.format(*options))
        option = input()

    if options[option]:
        return step2_umbrella()
    return step2_no_umbrella()


def step2_umbrella():
    print(
        'Утка-маляр с зонтиком заходит в бар',
        'Бармен: - Что будете пить?',
        sep='\n'
    )
    drink = input()
    print(
        f'Бармен наливает {drink} и говорит:',
        '- Тут недалеко есть цирк, не хотите пойти туда работать?',
        'Утка: - Говорящей уткой?',
        'Бармен: - Нет, маляром, конечно. Говорить все умеют.',
        sep='\n'
    )


def step2_no_umbrella():
    print(
        'Утка-маляр 🦆 без зонта заходит в бар',
        'Бармен: - Это бар только для уток',
        'Утка-маляр: - Я утка-маляр',
        'Бармер: - Вы выглядите как утка, ходите как утка, покрякайте: ',
        sep='\n'
    )
    voice = input()
    if 'кря' in voice:
        print(
            'Бармен наливает стакан водки.'
        )
    elif 'quack' in voice:
        print(
            'Бармен наливает рюмку виски.'
        )
    else:
        print(
            'Бармен: - Странный у вас акцент.',
            'Наливает бокал пива.',
            sep='\n'
        )


if __name__ == '__main__':
    step1()
