from collections import defaultdict
import csv
from typing import List, Dict


def main() -> None:
    """
    Загружает исходные данные
    выводит меню пользователя,
    в зависимости от выбора пользователя, вызывает
    различные функции
    """
    staff = read_csv('data/Corp_Summary.csv')

    print(
        'Выберите пункт меню:',
        '1. Вывести иерархию команд,'
        'т.е. департамент и все команды, которые входят в него',
        '2. Вывести сводный отчёт по департаментам: название, численность,'
        '"вилка" зарплат в виде мин – макс, среднюю зарплату',
        '3. Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.',
        sep='\n')

    options = {'1': lambda: print_hierarchy(staff),
               '2': lambda: print_report(get_stat(staff)),
               '3': lambda: save_report(get_stat(staff),
                                        input('Введите имя файла: '))
               }

    option = ''
    while option not in options:
        print('Выберите: {}/{}/{}'.format(*options))
        option = input()

    options[option]()


def read_csv(filename: str, csv_separator: str = ';') -> List[Dict[str, str]]:
    """
    Читает csv-файл с отчётом о сотрудниках компании.
    Входные данные:
    filename - имя csv-файла данных
    csv_separator - разделитель полей csv-файла
    Возвращаемое значение:
    staff - список;
    элемент списка - словарь с ключами, полученными
    из строки заколовка csv-файла
    """
    with open(filename, 'r', encoding='utf-8') as inp_file:
        staff = list(csv.DictReader(inp_file, delimiter=csv_separator))

    return staff


def print_hierarchy(staff: List[Dict[str, str]]) -> None:
    """
    Выводит иерархию команд, т.е. департамент и все команды,
    которые входят в него
    Входные данные:
    staff - список словарей, полученный из функции read_csv
    """
    hierarchy = defaultdict(set)
    for member in staff:
        hierarchy[member['Департамент']].add(member['Отдел'])

    for department, teams in hierarchy.items():
        print(f'Входящие в департамент "{department}" команды:')
        print(*teams, sep=', ')


def get_stat(staff:  List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Готовит сводный отчёт по департаментам
    Входные данные:
    staff - список словарей, полученный из функции read_csv
    Возвращаемое значение:
    stat_report - список из словарей, содержащих:
    департамент, численность, мин зарплата, макс зарплата, средняя зарплата;
    """
    dep_salaries = defaultdict(list)
    for member in staff:
        dep_salaries[member['Департамент']].append(int(member['Оклад']))

    stat_report = []
    for department, salaries in dep_salaries.items():
        stat_report.append({
            'depart': department,
            'size': len(salaries),
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_salary': round(sum(salaries) / len(salaries), 2)
            })

    return stat_report


def print_report(stat_report: List[Dict[str, str]],
                 header: Dict[str, str] = {
                                'depart': 'Департамент',
                                'size': 'численность',
                                'min_salary': 'мин. зарплата',
                                'max_salary': 'макс. зарплата',
                                'avg_salary': 'средняя зарплата'
                 }) -> None:
    """
    Выводит сводный отчёт по департаментам
    Входные данные:
    stat_report - список статистических данных, возвращаемый get_stat
    header - заголовок таблицы
    """
    def print_line(info_dict: Dict[str, str]) -> None:
        """
        Печатает форматированную строку из словаря
        """
        for field in stat_report[0].keys():
            print(f'{info_dict[field]:<20}', end='')
        print()

    print_line(header)
    for record in stat_report:
        print_line(record)


def save_report(stat_report: List[Dict[str, str]],
                csv_filename: str,
                csv_separator: str = ';',
                header: Dict[str, str] = {
                                'depart': 'Департамент',
                                'size': 'численность',
                                'min_salary': 'мин. зарплата',
                                'max_salary': 'макс. зарплата',
                                'avg_salary': 'средняя зарплата'
                 }) -> None:
    """
    Сохраняет сводный отчёт по департаментам в csv файл
    Входные данные:
    stat_report - список статистических данных, возвращаемый get_stat
    csv_filename - имя файла для сохранения результатов
    csv_separator - разделитель полей в csv файле
    header - заголовок таблицы
    """
    with open(csv_filename, 'w', encoding='utf-8') as otp_file:
        dict_writer = csv.DictWriter(otp_file,
                                     fieldnames=stat_report[0].keys(),
                                     delimiter=csv_separator,
                                     lineterminator='\n')
        dict_writer.writerow(header)
        dict_writer.writerows(stat_report)


if __name__ == "__main__":
    main()
