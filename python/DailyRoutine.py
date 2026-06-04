from functools import wraps
from dataclasses import dataclass
import time
import weakref


def log_time(unit='ms'):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start
            if unit == 'ms':
                print(f"{func.__name__}: {duration*1000:.2f} ms")
            elif unit == 's':
                print(f"{func.__name__}: {duration:.4f} s")
            return result
        return wrapper
    return decorator

class DailyRoutine():
    __slots__ = ("water_ml", "steps", "exercise_min", "pages_read", "_coffee_mg", "_owner")

    def __init__(self, owner=None):
        self.water_ml = 0
        self.steps = 0
        self.exercise_min = 0
        self.pages_read = 0
        self._coffee_mg = 0
        
        if owner:
            self._owner = weakref.ref(owner)
        else:
            self._owner = None

    def check_list():
        tasks = ["Drink Water", "Walk", "Exercise", "Read", "Coffee"]
        for task in tasks:
            yield task

    def __iter__(self):
        yield from DailyRoutine.check_list()

    @log_time()
    def __call__(self, action: str, amount: int) -> None:
        if action == None:
            raise ValueError("Choose action to do")

        if amount == None:
            raise ValueError("Write amount of your action")

        match action:
            case "Drink":
                self.water_ml += amount
            case "Walk":
                self.steps += amount
            case "Exercise":
                self.exercise_min += amount
            case "Read":
                self.pages_read += amount
            case "Coffee":
                self.coffee_mg += amount
            case _:
                raise ValueError("No such action: ", action)
    
    @property
    def coffee_mg(self):
        return self._coffee_mg

    @coffee_mg.setter
    def coffee_mg(self, value):
        if value > 400:
            raise ValueError("Слишком много кофеина!")
        self._coffee_mg = value

@dataclass
class Person():
    name: str

def main():
    person = Person(name="name")
    routine = DailyRoutine(owner=person)
    for i in routine:
        print(i)

    routine("Walk", 10000)
    routine("Coffee", 10000)

if __name__ == "__main__":
    main()