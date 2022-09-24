def main():
    """
    Загружает исходные данные
    выводит меню пользователя,
    в зависимости от выбора пользователя, вызывает
    различные функции
    """
    staff = read_csv('data/Corp_Summary.csv')
    stat_report = get_stat(staff)

    print(
        'Выберите пункт меню:',
        '1. Вывести иерархию команд,'
        'т.е. департамент и все команды, которые входят в него',
        '2. Вывести сводный отчёт по департаментам: название, численность,'
        '"вилка" зарплат в виде мин – макс, среднюю зарплату',
        '3. Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.',
        sep='\n')
    option = ''
    options = ['1', '2', '3']
    while option not in options:
        print('Выберите: {}/{}/{}'.format(*options))
        option = input()

    if option == '1':
        print_hierarchy(staff)
    elif option == '2':
        print_report(stat_report)
    else:
        save_report(stat_report, input('Введите имя файла: '))


def read_csv(filename: str, csv_separator: str = ';') -> list:
    """
    Читает csv-файл с отчётом о сотрудниках компании.
    Входные данные:
    filename - имя csv-файла данных
    csv_separator - разделитель полей csv-файла
    Возвращаемое значение:
    staff - список;
    элемент списка - словарь с ключами:
    'name', 'department', 'team', 'position', 'grade', 'salary'
    """
    fields = ['name', 'department', 'team', 'position', 'grade', 'salary']
    staff = []
    with open(filename, 'r', encoding='utf-8') as inp_file:
        inp_file.readline()  # пропускаем заголовок csv-файла
        for line in inp_file:
            staff.append({key: value for key, value in
                          zip(fields, line.strip().split(csv_separator))})
    return staff


def print_hierarchy(staff: list):
    """
    Выводит иерархию команд, т.е. департамент и все команды,
    которые входят в него
    Входные данные:
    staff - список, полученный из функции read_csv
    """
    hierarchy = {}
    for member in staff:
        hierarchy.setdefault(member['department'], set()).add(member['team'])

    for department, teams in hierarchy.items():
        print(f'Входящие в департамент "{department}" команды:')
        print(*teams, sep=', ')


def get_stat(staff: list) -> list:
    """
    Готовит сводный отчёт по департаментам
    Входные данные:
    staff - двумерный список, полученный из функции read_csv
    Возвращаемое значение:
    stat_report - список из списков, содержащих:
    департамент, численность, мин зарплата, макс зарплата, средняя зарплата;
    первый элемент списка - список заголовков
    """
    dep_salaries = {}
    for member in staff:
        dep_salaries.setdefault(member['department'], [])\
            .append(int(member['salary']))

    stat_report = [['Департамент', 'численность', 'мин. зарплата',
                    'макс. зарплата', 'средняя зарплата']]
    for department, salaries in dep_salaries.items():
        stat_report.append([department, len(salaries), min(salaries),
                            max(salaries),
                            round(sum(salaries) / len(salaries), 2)])

    return stat_report


def print_report(stat_report: list):
    """
    Выводит сводный отчёт по департаментам
    Входные данные:
    stat_report - список статистических данных, возвращаемый get_stat
    """
    for line in stat_report:
        print('{:<20}{:<20}{:<20}{:<20}{:<20}'.format(*line))


def save_report(stat_report: list, csv_filename: str,
                csv_separator: str = ';'):
    """
    Сохраняет сводный отчёт по департаментам в csv файл
    Входные данные:
    stat_report - список статистических данных, возвращаемый get_stat
    csv_filename - имя файла для сохранения результатов
    csv_separator - разделитель полей в csv файле
    """
    with open(csv_filename, 'w', encoding='utf-8') as otp_file:
        for line in stat_report:
            print(*line, sep=csv_separator, file=otp_file)


if __name__ == "__main__":
    main()
