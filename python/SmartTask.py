from dataclasses import dataclass
from functools import wraps


@dataclass
class SmartTask():
    title: str = ""
    priority: int = 0
    state: str = ""

    def __post_init__(self):
        '''Пост инит для запуска валидаторов'''
        self.title = self.__validate_title(self.title)

    def _log_changes(changer: callable) -> callable:
        '''Логгирует изменения сеттеров для тасок'''
        @wraps(changer)
        def func(self, *args, **kwargs):
            changer(self, *args, **kwargs)
            print("Изменено: ", *args, **kwargs)
        return func

    @_log_changes
    def setState(self, new_state: str) -> None:
        '''Изменяет состояние таски'''
        self.state = new_state
    
    @_log_changes
    def setPriority(self, new_priority: str) -> None:
        '''Изменяет приоритет таски'''
        self.priority = new_priority
   
    @property
    def is_urgent(self) -> bool:
        '''Срочная ли задача'''
        return self.priority >= 5
    
    @staticmethod
    def __validate_title(title: str) -> str:
        '''Проверка длинны названия таски (<= 100symb)'''
        if len(title) > 100:
            raise Exception(f"{title[:100]} - cлишком длинное название (более 100 символов)")
        return title
    
    @classmethod
    def from_string(cls, data: str) -> SmartTask:
        '''Конструктор из строки'''
        data = data.split(";")
        return SmartTask(data[0], int(data[1]))

    def __enter__(self) -> None:
        '''Начало выполнения задачи'''
        self.setState("В процессе")
        print("Начинаю задачу: ", self.title)

    def __exit__(self, exc_type, exc, exc_tb) -> None:
        '''Окончание выполнения задачи'''
        if exc_type is None:
            self.setState("Выполнена")
            print("Заканчиваю задачу: ", self.title)
            return 
        self.setState("Возникла ошибка при выполнении")
        print("Возникла ошибка при выполнении: ", exc_type, exc)

    def __eq__(self, value: SmartTask) -> bool:
        '''Равенство тасок (по названию)'''
        return self.title == value.title

    def __lt__(self, other: SmartTask) -> bool:
        '''Меньше ли таска по приоритету'''
        return self.priority < other.priority

    def __str__(self) -> str:
        '''Название таски'''
        return self.title

    def __call__(self) -> str:
        '''Статус таски'''
        return f"Задача {self.state}: {self.title}"

    # repr уже встроен в dataclass
    
def main():
    task1 = SmartTask("Первая задачка", 1, "Не выполнено")
    task2 = SmartTask("Вторая задачка", 2, "В процессе")
    task3 = SmartTask.from_string("Третья задачка;3")

    print(task1)
    print(repr(task1))

    print(task1.is_urgent)

    print(task1 == task2)
    print(task1 < task2)
    print(task2 < task1)

    task1.setPriority(2)
    task1.setState("В процессе")

if __name__ == "__main__":
    main()