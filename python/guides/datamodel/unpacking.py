lax_coordeinates = (33.3, -118.8)

lattitude, longitude = lax_coordeinates
print(lattitude, longitude)

# --------------- swap

a, b = 1, 2
a, b = b, a

# --------------- func 1

print(divmod(20, 8))

t = (20, 8)
print(divmod(*t))

quotient, remainder = divmod(*t)
print(quotient, remainder)

# --------------- func 2

import os

_, filename = os.path.split('C:/Users/farfromsouls/test.txt')
print(filename)

# --------------- rest elements

a, b, *rest = range(5)
print(a, b, rest)

a, b, *rest = range(2)
print(a, b, rest)

a, *rest, b = range(5)
print(a, rest, b)

*rest, a, b = range(5)
print(rest, a, b)

# --------------- func 3!

def fun(a, b, c, d, *rest):
    return a, b, c, d, rest

print(fun(*[1, 2], 3, *range(4, 7)))

# --------------- deep obj unpack


areas = [
    ("1", "2", "3", (1, 2)),
    ("2", "2", "3", (2, 2)),
    ("3", "2", "3", (3, 2)),
    ("4", "2", "3", (4, 2))
]
print(f'{"":15} | {"lattitude":>9} | {"longitude":>9}')
for name, _, _, (lat, lon) in areas:
    print(f'{name:15} | {lat:9.4f} | {lon:9.4f}')