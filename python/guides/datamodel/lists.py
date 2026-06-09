x = 'ABC'
codes = [last := ord(c) for c in x]
print(last)

symbols = '$¢¥₤€'
beyond_ascii = [ord(s) for s in symbols if ord(s) > 127]
print(beyond_ascii)

beyond_ascii = list(filter(lambda c: c > 127, map(ord, symbols)))
print(beyond_ascii)

# Декартовы произведения

colors = ['black', 'white']
sizes = ['S', 'M', 'L']

tshirts = [(color, size) for color in colors for size in sizes]
print(tshirts)

# Генераторные выражения

import array

print(tuple(ord(symbol) for symbol in symbols))
print(array.array('I', (ord(symbol) for symbol in symbols)))

for tshirt in (f'{c} {s}' for c in colors for s in sizes):
    print(tshirt)

# Кортежи как записи
lax_coordinates = (33.9425, -118.408056)
city, year, pop, chg, area = ('Tokyo', 2003, 32_450, 0.66, 8014)
traveler_ids = [('USA', '123123123'), ('BRA', '234234234'), ('ESP', '3453455345')]

for passport in sorted(traveler_ids):
    print("%s/%s" % passport)

for country, _ in traveler_ids:
    print(country)