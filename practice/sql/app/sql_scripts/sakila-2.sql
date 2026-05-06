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
