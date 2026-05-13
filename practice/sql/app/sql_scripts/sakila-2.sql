-- ========================================================================
-- Теория множеств

-- 1) При объединении множеств оба набора данных должны иметь одинаковое кол-во столбцов
-- 2) Типы данных в соответствующих столбцах должны совпадать
SELECT 1 num, 'abs' str
UNION
SELECT 9 num, 'xyz' str;

-- UNION - сортирует объекты и удаляет дубликаты,
-- UNION ALL - не делает этого
-- SELECT 'CUST' typ, c.first_name, c.last_name
-- FROM customer AS c
-- UNION
-- SELECT 'ACTR' typ, a.first_name, a.last_name
-- FROM actor AS a;

-- Пример показывающий что ALL сохраняет дубликаты (объединение одной и той же таблицы)
-- SELECT 'CUST' typ, c.first_name, c.last_name
-- FROM customer AS c
-- UNION ALL
-- SELECT 'CUST' typ, c.first_name, c.last_name
-- FROM customer AS c

-- ОБЪЕДИНЕНИЕ UNION Люди из 2х таблиц, у которых инициалы JD 
SELECT c.first_name, c.last_name
FROM customer AS c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
UNION ALL -- (С ПОВТОРЕНИЯМИ!)
SELECT a.first_name, a.last_name
FROM actor AS a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%';

-- ПЕРЕСЕЧЕНИЕ INTERSECT актеров с инициалами JD и покупателей JD 
SELECT c.first_name, c.last_name
FROM customer AS c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
INTERSECT 
SELECT a.first_name, a.last_name
FROM actor AS a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%';

-- ИСКЛЮЧЕНИЕ EXCEPT актеров JD, кроме тех, у которых инициалы совпадают с кем то из покупателей
SELECT a.first_name, a.last_name
FROM actor AS a
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
EXCEPT
SELECT c.first_name, c.last_name
FROM customer AS c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%';

-- Существуют except all и intersect all, но они реализованны только в 
-- IBM DB2 Universal Server

-- ========================================================================
-- Правила применения операторов для работы с множествами

-- Order By для составного запроса:
SELECT a.first_name AS fname, a.last_name AS lname 
FROM actor AS a 
WHERE a.first_name LIKE 'J%' AND a.last_name LIKE 'D%'
UNION ALL
SELECT c.first_name, c.last_name  
FROM customer AS c
WHERE c.first_name LIKE 'J%' AND c.last_name LIKE 'D%'
ORDER BY lname, fname;
-- Пояснение: для orderby нельзя использовать имена столбцов из
-- второго запроса, если бы order by был по last_name и first_name
-- мы получили бы ошибку Unknown column

-- Так же надо помнить о приоритете операторов работы над множествами


-- ========================================================================
-- Упражнение 6.2 + 6.3
SELECT first_name, last_name
FROM customer
WHERE customer.last_name LIKE 'L%'
UNION
SELECT first_name, last_name
FROM actor
WHERE actor.last_name LIKE 'L%'
ORDER BY last_name;

-- ========================================================================
-- ГЕНЕРАЦИЯ, ОБРАБОТКА И ПРЕОБРАЗОВАНИЕ ДАННЫХ

CREATE TABLE string_tbl (
    char_fld CHAR(30),
    vchar_fld VARCHAR(30),
    text_fld TEXT
);

INSERT INTO string_tbl (char_fld, vchar_fld, text_fld)
VALUES (
    'This is char data',
    'This is varchar data',
    'This id text data'
);

-- В старых версиях MySQL поведение было не строгим (ANSI)
-- Т.Е. при создании слишком длинной строки она усекалась и было предупреждение
-- а с версии 6.0 мы получаем полноценную ошибку
-- узнать в каком мы режиме (строгом или нет) можно с помощью:
SELECT @@session.sql_mode;

-- переключение на ANSI:
SET sql_mode='ansi';
SELECT @@session.sql_mode;

UPDATE string_tbl
SET vchar_fld = 'This id a piece of extremely long data';

SHOW WARNINGS;

SELECT vchar_fld
FROM string_tbl;