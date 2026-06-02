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

-- Включение одинарных ковычек
UPDATE string_tbl
SET text_fld = 'this string '' works';
-- и SET text_fld = 'this string \' works' для Oracle и MySQL;

SELECT quote(text_fld)
FROM string_tbl;

-- Включение спец. символов
SELECT 'abcdefg', char(97, 98, 99, 100, 101, 102, 103);
-- зависит от набора символов, естественно

-- Способ конкатенации строк зависит от сервера который используем
SELECT CONCAT('danke sch', CHAR(149), 'n');
SELECT 'danke sch' + CHAR(149) + 'n';

SELECT ASCII('a');

SELECT LENGTH(char_fld), LENGTH(vchar_fld), LENGTH(text_fld)
FROM string_tbl;

INSERT INTO string_tbl (char_fld, vchar_fld, text_fld)
VALUES (
    'This string is 28 characters',
    'This string is 28 characters',
    'This string is 28 characters'
);

-- Поиск индекса подстроки
SELECT POSITION('characters' IN vchar_fld)
FROM string_tbl;

-- Поиск индекса подстроки начиная с определенного индекса
SELECT LOCATE('is', vchar_fld, 5)
FROM string_tbl;

-- strcmp (-1 если первая строка предшествует второй, 0 если идентичны, 1 если первая после второй)
-- Доступна только в MySQL
DELETE FROM string_tbl;

INSERT INTO string_tbl (vchar_fld)
VALUES ('abcd'), ('xyz'), ('QRSTUV'), ('qrstuv'), ('12345');

SELECT vchar_fld 
FROM string_tbl
ORDER BY vchar_fld;

SELECT STRCMP('12345', '12345') AS 12345_12345,
    STRCMP('abcd', 'xyz') AS abcd_xyz,
    STRCMP('abcd', 'QRSTUV') AS abcd_QRSTUV,
    STRCMP('qrstuv', 'QRSTUV') AS qrstuv_QRSTUV,
    STRCMP('12345', 'xyz') AS 12345_xyz,
    STRCMP('xyz', 'qrstuv') AS xyz_qrstuv;

-- Так же MySQL позволяет использовать в select like и regexp
SELECT name, name LIKE '%y' AS ends_in_y
FROM category;

SELECT name, name REGEXP 'y$' AS ends_in_y
FROM category;

-- Строковые функции возвращающие строки

-- Добавление текста к строкам через CONCAT
DELETE FROM string_tbl;

INSERT INTO string_tbl (text_fld)
VALUES ('This string was 29 characters');

UPDATE string_tbl
SET text_fld = CONCAT(text_fld, ', but now it is longer');

SELECT text_fld
FROM string_tbl;

-- Таким же образом часто меняют не сами строки в таблице
-- А вывод запроса
SELECT CONCAT(first_name, ' ', last_name, ' has been a customer since ', date(create_date)) cust_narrative
FROM customer;

-- Такой метод не работает в Oracle, но есть просто оператор конкатенации
-- SELECT first_name || ' ' || last_name || ' ' || ' has been a customer since ' || date(create_date) AS cust_narrative
-- FROM customer;

-- Существует функция insert, она помогает не с добавлением, а с заменой/вставкой

SELECT INSERT('goodbye world', 9, 0, 'cruel ') AS string;
-- goobye cruel world

SELECT INSERT('goodbye world', 1, 7, 'hello') AS string;
-- hello world

-- Аналог в Oracle REPLACE:
SELECT REPLACE('goodbye world', 'goodbye', 'hello');

-- SQL Server stuff такая же как insert в MySQL
-- SELECT STUFF('hello world', 1, 5, 'goodbye cruel');

SELECT SUBSTRING('goodbye cruel world', 9, 5);

-- ========================================================================
-- Работа с числовыми данными

SELECT (37 * 59) / (78 - (8 * 6));

-- ДОСТУПНЫЕ ФУНКЦИИ:
-- acos(x)
-- asin(x)
-- atan(x)
-- cos(x)
-- cot(x)
-- exp(x)
-- ln(x)
-- sin(x)
-- sqrt(x)
-- tan(x)

-- Целочисленное деление mod
SELECT MOD(10, 4);
SELECT MOD(22.75, 5);

-- POW
SELECT POW(2, 8);

SELECT POW(2, 10) AS kilobyte, 
       POW(2, 20) AS megabyte,
       POW(2, 30) AS gigabyte, 
       POW(2, 40) AS terabyte;

-- Управление точностью чисел

-- Округление ceil, floor и round 
SELECT CEIL(72.445), FLOOR(72.445);
SELECT ROUND(72.445), ROUND(72.545);

-- Точность
SELECT ROUND(72.445, 1), ROUND(72.445, 2), ROUND(72.445, 3);

-- Есть так же функция truncate - она не занимается округдением, она
-- только отбрасывает знаки после запятой
SELECT TRUNCATE(72.445, 1), TRUNCATE(72.445, 2), TRUNCATE(72.445, 3);

-- Так же для случаев если например пользователь хочет заказать 17 единиц
-- продукта, а у нас продается либо только 10 или только 20, то можно
-- использовать отрицательные значения
SELECT ROUND(17, -1), TRUNCATE(17, -1);

-- Работа с знаковыми данными
SELECT SIGN(-10), SIGN(0), SIGN(10);
--           -1        0         1 
SELECT ABS(-10);

-- ========================================================================
-- Часовые пояса

-- MySQL хранит в настройках 2 часовых пояса:
-- часовой пояс непосредственно сервера
-- часовой пояс сессии с пользователем (с разными пользователями бывают разные)
SELECT @@global.time_zone, @@session.time_zone;

-- Значение SYSTEM - означает что сервер использует настройку пояса
-- в котором находится база данных

SET time_zone = 'Europe/Zurich';
SELECT @@global.time_zone, @@session.time_zone;

-- В Oracle можно поменять session timezone с помощью ALTER

-- ГЕНЕРАЦИЯ ВРЕМЕННЫХ ДАННЫХ
-- Способы:

-- 1) копирование данных существующего столбца 
-- 2) выполнение встроенной функции вощвращающей время
-- 3) построение строкового представления временных данных для вычисления сервером

UPDATE rental
SET return_date = '2019-09-17 15:30:00'
WHERE rental_id = 9999;

-- Преобразование строки в дату
SELECT CAST('2019-09-17 15:30:00' AS DATETIME);

SELECT CAST('2019-09-17' AS DATE) AS date_field,
    CAST('15:30:00' AS TIME) AS time_field;

-- Функции геренации дат
UPDATE rental
SET return_date = STR_TO_DATE('September 17, 2019', '%M %d, %Y')
WHERE rental_id = 99999;

-- Текущие дата и время
SELECT CURRENT_DATE(), CURRENT_TIME(), CURRENT_TIMESTAMP();

-- Манипуляции временными данными
SELECT DATE_ADD(CURRENT_DATE(), INTERVAL 5 DAY);

-- Представим что нам надо поправить временные данные
-- И нам удобнее сделать это относительно, например:
-- Нам сказали что фильм вернули на 3 часа 27 минут 11 секунд позже
-- Чем было указано изначально
-- Тогда:
UPDATE rental
SET return_date = DATE_ADD(return_date, INTERVAL '3:27:11' HOUR_SECOND)
WHERE rental_id = 99999;

-- Или например мы выяснили что сотрудник с идентификатором
-- 4789 в базе данных старше, чем на самом деле
-- Добавим к его дате рождения 9 лет 11 месяцев
-- UPDATE employee
-- SET birth_date = DATE_ADD(birth_date, INTERVAL '9-11' YEAR_MONTH)
-- WHERE emp_id = 4789;

-- Удобный способ узнавать последний день месяца:
SELECT LAST_DAY('2019-09-17');

-- Функции возвращающие строки
SELECT DAYNAME('2019-09-18');
SELECT EXTRACT(YEAR FROM '2019-09-18 22:19:05');

-- Функции возвращающие числовые значения
SELECT DATEDIFF('2019-09-03', '2019-06-21');
SELECT DATEDIFF('2019-09-03 23:59:59', '2019-06-21 00:00:01');
SELECT DATEDIFF('2019-06-21', '2019-09-03');

-- Функции преобразования
SELECT CAST('1456328' AS SIGNED INTEGER);
SELECT CAST('123ABC999' AS UNSIGNED INTEGER);
show warnings;

-- Упражнение 7.1
SELECT SUBSTRING('Please find the substring in this string', 17, 8);

-- Упражнение 7.2
SELECT ABS(-25.76823), SIGN(-25.76823);

-- Упражнение 7.3
SELECT EXTRACT(MONTH FROM CURRENT_DATE()); 
