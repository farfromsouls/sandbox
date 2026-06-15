a = (10, 'alpha', [1, 2])
b = (10, 'alpha', [1, 2])
print(a == b)

b[-1].append(99)
print(a == b)

print(b)

# ---------------------------

def fixed(o):
    try:
        hash(o)
    except TypeError:
        return False
    return True

tm = (10, 'alpha', (1, 2))
tf = (10, 'alpha', [1, 2])
fixed(tf)
fixed(tm)

