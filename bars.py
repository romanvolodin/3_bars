import argparse
import json
import math


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_data',
                        help='path to bars data in json format')
    return parser.parse_args()


def load_data(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        exit("Ошибка: Файл {} не найден.".format(filepath))
    except PermissionError:
        exit("Ошибка: Нехватает прав для чтения файла {}.".format(filepath))
    except json.decoder.JSONDecodeError:
        exit("Ошибка: Файл {} не содержит json данные.".format(filepath))


def get_biggest_bar(json_data):
    return max(
        json_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_smallest_bar(json_data):
    return min(
        json_data,
        key=lambda bar: bar['properties']['Attributes']['SeatsCount']
    )


def get_closest_bar(json_data, user_long, user_lat):
    return min(
        json_data,
        key=lambda bar: get_distance(bar, user_long, user_lat)
    )


def print_bar(bar, bar_type):
    bar = bar['properties']['Attributes']

    bar_template = '''
    Самый {type} бар:
    {name}
    Телефон: {phone}
    Адрес: {address}
    Число мест: {seats}'''

    print(bar_template.format(
        type=bar_type.lower(),
        name=bar['Name'],
        phone=bar['PublicPhone'][0]['PublicPhone'],
        address=bar['Address'],
        seats=bar['SeatsCount'],
    ))


def get_distance(bar, user_long, user_lat):
    bar_lat, bar_long = bar['geometry']['coordinates']
    return math.sqrt(
        (bar_long - user_long) ** 2 + (bar_lat - user_lat) ** 2
    )


if __name__ == '__main__':
    args = parse_arguments()
    path = args.input_data
    json_data = load_data(path)['features']

    print('Введите ваши координаты и мы покажем ближайший бар!\n'
          'Координаты удобно скопировать в картах Гугла или Яндекса.\n'
          'Например: 55.752631, 37.621418')

    user_input = input().strip()
    
    try:
        user_long, user_lat = user_input.split(', ')
        user_long = float(user_long)
        user_lat = float(user_lat)
    except ValueError:
        exit('Ошибка: Координаты должны быть в формате: XX.XXX, YY.YYY')

    closest_bar = get_closest_bar(json_data, user_long, user_lat)
    biggest_bar = get_biggest_bar(json_data)
    smallest_bar = get_smallest_bar(json_data)

    print_bar(closest_bar, 'близкий')
    print_bar(biggest_bar, 'большой')
    print_bar(smallest_bar, 'маленький')

