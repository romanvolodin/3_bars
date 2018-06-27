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


def get_closest_bar(data, longitude, latitude):
    return min(
        data['features'],
        key=lambda item: math.sqrt(
            (item['geometry']['coordinates'][1] - longitude)**2 + (item['geometry']['coordinates'][0] - latitude)**2
        )
    )


if __name__ == '__main__':
    path = "bars.json"
    data = load_data(path)
    biggest = get_biggest_bar(data)['properties']['Attributes']
    smallest = get_smallest_bar(data)['properties']['Attributes']
    closest = get_closest_bar(data, 55.667587, 37.556106)
    print(closest)
