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
    except json.decoder.JSONDecodeError:
        return


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


def get_user_coordinates():
    print('Введите ваши координаты и мы покажем ближайший бар!\n'
          'Координаты удобно скопировать в картах Гугла или Яндекса.\n'
          'Например: 55.752631, 37.621418')

    user_input = input().strip()

    try:
        user_long, user_lat = user_input.split(', ')
        user_long = float(user_long)
        user_lat = float(user_lat)
        return user_long, user_lat
    except ValueError:
        return


if __name__ == '__main__':
    args = parse_arguments()
    path = args.input_data

    try:
        bars_data = load_data(path)
    except (FileNotFoundError, PermissionError) as err:
        exit(err)

    if bars_data is None:
        exit('Ошибка: Невозможно прочитать файл {}. Убедитесь, что файл '
             'содержит json данные.'.format(path))
    bars = bars_data['features']

    user_coordinates = get_user_coordinates()
    if user_coordinates is None:
        exit('Ошибка: Координаты должны быть в формате: XX.XXX, YY.YYY')
    user_long, user_lat = user_coordinates

    closest_bar = get_closest_bar(bars, user_long, user_lat)
    biggest_bar = get_biggest_bar(bars)
    smallest_bar = get_smallest_bar(bars)

    print_bar(closest_bar, 'близкий')
    print_bar(biggest_bar, 'большой')
    print_bar(smallest_bar, 'маленький')

