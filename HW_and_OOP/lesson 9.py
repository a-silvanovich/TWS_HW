import json, csv, os

with open('city.list.json', "r", encoding='utf-8') as city_json:
    city_data = json.load(city_json)
# print(city_data[0])

# Задание 1

print(f'Cities number: {len(city_data)}')

# Задание 2

country_number = {}        #Словарь страна_число городов
for city in city_data:
    country_number.setdefault(city['country'], 0)
    country_number[city['country']] += 1

# Задание 3

south_cities = 0
north_cities = 0
for city in city_data:
    if city["coord"]["lat"] > 0:
        north_cities += 1
    else:
        south_cities += 1
# print(north_cities, south_cities)

# Задание 4

with open('city.list.csv', "w", encoding='utf-8', newline='') as city_csv:
    writer = csv.DictWriter(city_csv, fieldnames=list(city_data[0].keys()))
    writer.writeheader()
    for city in city_data:
        writer.writerow({
            'id': city['id'],
            'name': city['name'],
            'country': city['country'],
            'coord': f'{city["coord"]["lat"]}, {city["coord"]["lon"]}',
        })

# Задание 5

selected_country = input('Введите индекс страны: ')
selected_cities = []
for city in city_data:
    if city['country'] == selected_country:
        selected_cities.append(city)
with open('selected_country.json', "w", encoding='utf-8', newline='') as selected_json:
    json.dump(selected_cities, selected_json, indent=4)

# Задание 6

# os.mkdir('cities_by_country')

def create_city_list(country_index):    #Создание списка городов определенной страны
    selected_list = []
    for city in city_data:
        if city['country'] == country_index:
            selected_list.append(city)
    return selected_list

countries = []
for city in city_data:
    if city['country'] not in countries:
        countries.append(city['country'])
for index in countries:
    cities_list = create_city_list(index)
    with open(f'cities_by_country/{index}_cities.json', "w", newline='') as cities_json:
        json.dump(cities_list, cities_json)

# Задание 7

geo = {
    "type": "FeatureCollection",
    "features": []
}
cities_BY = create_city_list('BY')
for city in cities_BY[:100]:
    geo['features'].append({
        "type": "Feature",
        "id": city['id'],
        "geometry":
            {"type": "Point",
            "coordinates": [city['coord']['lon'], city['coord']['lat']]},
        "properties": {
            "description": city['name'],
            "iconCaption": city['name'],
            "marker-color": "#FF0000"
        }
    })
# print(geo)
with open('cities_BY.geojson', 'w', encoding='utf-8', newline='') as geojson:
    json.dump(geo, geojson, indent=4)