import json
import math


def load_data(filepath):
    with open(filepath, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def get_biggest_bar(data):
    return max(
        data['features'],
        key=lambda item: item['properties']['Attributes']['SeatsCount']
    )


def get_smallest_bar(data):
    return min(
        # I think SeatsCount == 0 means "no data"
        # so I ignore such bars
        [
            item for item in data['features']
            if int(item['properties']['Attributes']['SeatsCount']) > 0
        ],
        key=lambda item: item['properties']['Attributes']['SeatsCount']
    )


def get_closest_bar(data, long, lat):
    # The geo coordinates in the json data seem to be mixed up.
    # For example:
    # the first bar coordinates are [37.621587946152012, 55.765366956608361],
    # but Yandex says it should be [55.765366956608361, 37.621587946152012].

    geo = 'geometry'
    coords = 'coordinates'
    return min(
        data['features'],
        key=lambda item: math.sqrt(
            (item[geo][coords][1] - long)**2 + (item[geo][coords][0] - lat)**2
        )
    )


if __name__ == '__main__':

    def print_bar(bar, bar_type):
        bar = bar['properties']['Attributes']
        print(bar_template.format(
            type=bar_type.lower(),
            name=bar['Name'],
            phone=bar['PublicPhone'][0]['PublicPhone'],
            address=bar['Address'],
            seats=bar['SeatsCount'],
        ))


    bar_template = '''
Самый {type} бар:
{name}
Телефон: {phone}
Адрес: {address}
Число мест: {seats}'''

    message = '''
Введите ваши координаты и мы покажем ближайший бар!
Координаты удобно скопировать в картах Гугла или Яндекса.
Например: 55.752631, 37.621418
'''

    path = "bars.json"
    data = load_data(path)

    print(message, end='')

    while True:
        user_input = input().strip()
        try:
            user_long, user_lat = user_input.split(', ')
            user_long = float(user_long)
            user_lat = float(user_lat)
            break
        except ValueError:
            print('Координаты должны быть в формате: XX.XXX, YY.YYY')

    closest = get_closest_bar(data, user_long, user_lat)
    biggest = get_biggest_bar(data)
    smallest = get_smallest_bar(data)

    print_bar(closest, 'близкий')
    print_bar(biggest, 'большой')
    print_bar(smallest, 'маленький')

