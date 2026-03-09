import os
import time
import re
import random


TEXT_ENCODING = "utf-8"


def read_text(encoding) -> list: 
    file = open("words.txt", "r", encoding=encoding)
    text = file.read()
    words = re.split(" |\n", text)
    return words

def random_word(words) -> str:
    return words[random.randint(0, len(words)-1)]

def random_words(words, amount) -> list:
    return [random_word(words) for i in range(amount)]

def analyse_text(user_words, task_words, task_time) -> dict:
    analyse = {
        "symbPerMin": None,
        "errors": None,
        "accuracy": None,
        "timePerWord": None
    }

    len_tw = len(task_words)
    ran_len_tw = range(len_tw)
    cond = [user_words[i]==task_words[i] for i in ran_len_tw]
    symb = len(" ".join(task_words))

    analyse["symbPerMin"] = round(symb/task_time * 60, 0)
    analyse["errors"] = cond.count(False)
    analyse["accuracy"] = round((cond.count(True)/len_tw)*100, 1)
    analyse["timePerWord"] = round(task_time/len_tw, 1)
    return analyse

def gameloop(words) -> int:
    amount = input("Введите желаемое количество слов: ")
    if amount == "":
        print("Спасибо за игру!!")
        time.sleep(3)
        return 0
    try:
        amount = int(amount)
    except:
        print("Неверное кол-во слов!")
        time.sleep(1)
        return 1

    task_words = random_words(words, amount)
    task = ' '.join(task_words)
    os.system("cls")
    print(f"\n{task}\n")
    time.sleep(2)

    for i in range(3, 0, -1):
        print(f"{i}...")
        time.sleep(2)

    os.system("cls")
    print(f"{task}\n")
    print("Старт!!!\n")

    time_start = time.time()
    user_words = input().split(" ")
    time_finish = time.time()

    task_time = round(time_finish-time_start, 2)
    analyse = analyse_text(user_words, task_words, task_time)

    print(f"\nСуммарное время: {round(task_time, 1)}c\n"
        + f"Символов в минуту: {analyse['symbPerMin']}\n"
        + f"Ошибок: {analyse['errors']}\n"
        + f"Точность: {analyse['accuracy']}%\n"
        + f"Время на одно слово: {analyse['timePerWord']}c\n")

def main(encoding) -> int:
    os.system("cls")
    print("Загрузка слов...")
    words = read_text(encoding)

    lenwords = len(words)
    if lenwords == 0:
        os.system("cls")
        print("Возникла ошибка, проверьте words.txt")
        return 1
    print("Слова успешно загруженны\n")

    while True:
        game = gameloop(words)
        if game == 0:
            return 0


if __name__ == "__main__":
    main(TEXT_ENCODING)