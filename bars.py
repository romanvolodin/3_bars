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
    path = "bars.json"
    data = load_data(path)
    biggest = get_biggest_bar(data)['properties']['Attributes']
    smallest = get_smallest_bar(data)['properties']['Attributes']
    closest = get_closest_bar(data, 55.667587, 37.556106)
    print(closest)
