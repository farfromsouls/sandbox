-- вернет пустое множество
SELECT first_name, last_name 
    FROM customer
    WHERE last_name = 'ZIEGLER';

SELECT * FROM category;

-- дополнительные литералы/выражения/вызовы которые можно вставлять в SELECT
-- тут так же рассмотрено использование ПСЕВДОНИМОВ для столбцов
SELECT language_id,
    'COMMON' language_usage,
    language_id*3.1415927 lang_pi_value,
    upper(name) language_name
FROM language;

-- показательный пример что для запроса достаточно и одного SELECT
SELECT version(),
    user(),
    database();

-- лучше даже подчеркнуть применение псевдонимов с помощью AS
SELECT language_id,
    'COMMON' AS language_usage,
    language_id*3.1415927 AS lang_pi_value,
    upper(name) AS language_name
FROM language;

-- SELECT actor_id FROM film_actor ORDER BY actor_id;
-- вернуло бы 5462 строки с дубликатами т.к. одни актеры могли сниматься в нескольких фильмах
-- поэтому надо получить множество РАЗЛИЧНЫХ актеров с помощью DISTINCT
SELECT DISTINCT actor_id FROM film_actor ORDER BY actor_id;
-- надо помнить что DISTINCT требует сортировки, поэтому надо осторожно применять его для больших наборов

-- Подзапросы
SELECT concat(cust.last_name, ', ', cust.first_name) AS full_name
FROM (
    SELECT first_name, last_name, email
    FROM customer
    WHERE first_name = 'JESSIE'
) AS cust;

-- Временные таблицы
CREATE TEMPORARY TABLE actors_j (
    actor_id smallint(5),
    first_name varchar(45),
    last_name varchar(45)
);

INSERT INTO actors_j
SELECT actor_id, first_name, last_name
FROM actor
WHERE last_name LIKE 'J%';

SELECT * FROM actors_j;

-- Представление - запрос который хранится в словаре данных 
-- Выглядит и действует как таблица, но данных нет (поэтому еще называют "виртуальной таблицей")
-- При выполнении запроса к представлению, выполняется объединение запроса с определением представления.
CREATE VIEW cust_vw AS
    SELECT customer_id, first_name, last_name, active
    FROM customer;

SELECT first_name, last_name
FROM cust_vw
WHERE active = 0;

-- ========================================================================
-- Связи таблиц (JOIN)
-- Простой пример:
SELECT customer.first_name, customer.last_name,
       time(rental.rental_date) AS rental_time
FROM customer
    INNER JOIN rental
    ON customer.customer_id = rental.customer_id
WHERE date(rental.rental_date) = '2005-06-14';
-- в ON мы указали связь через идентификатор клиента
-- Это УСЛОВИЕ СОЕДИНЕНИЯ двух таблиц

-- Чтобы понять в остальных предложения (кроме FROM где происходит JOIN)
-- к какой таблице мы обращаемся, можно использовать 2 метода:
-- 1) Использовать полное имя таблицы (пример: employee.emp_id)
-- 2) Назначить таблице псевдоним:
SELECT c.first_name, c.last_name,
       time(r.rental_date) AS rental_time
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14';

-- ========================================================================
-- Предложение WHERE - механизм для фильтрации нежелательных строк из вашего результирующего набора

-- Фильмы напрокат с рейтингом G которые можно держать от недели:
SELECT title 
FROM film
WHERE rating = 'G' AND rental_duration >= 7;

-- Более сложные условия
SELECT title, rating, rental_duration
FROM film
WHERE (rating = 'G' AND rental_duration >= 7)
    OR (rating = 'PG-13' AND rental_duration < 4);

-- ========================================================================
-- GROUP BY
-- Предположим я хочу получить всех клиентов, которые брали
-- напрокат 40 или более фильмов. Вместо того, чтобы просматривать
-- все 16044 строки в таблице rental я могу написать запрос, который дает 
-- указание серверу сгруппировать все записи проката по клиентам,
-- подсчитать количество для каждого клиента и вернуть только тех,
-- у которых это количество не меньше 40.
SELECT c.first_name, c.last_name, count(*)
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
GROUP BY c.first_name, c.last_name
HAVING count(*) >= 40;

-- ========================================================================
-- Сортировка ORDER BY (в алфавитном порядке)
SELECT c.first_name, c.last_name,
       time(r.rental_date) AS rental_time
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14'
ORDER BY c.last_name;

-- Дополнительные параметры сортировки (например, если есть однофамильцы)
SELECT c.first_name, c.last_name,
       time(r.rental_date) AS rental_time
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14'
ORDER BY c.last_name, c.first_name;

-- Сортировка по возрастанию/убыванию (asc desc)
SELECT c.first_name, c.last_name,
       time(r.rental_date) AS rental_time
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14'
ORDER BY time(r.rental_date) desc; -- убывание по времени

-- Сортировка с помощью номера столбца
SELECT c.first_name, c.last_name,
       time(r.rental_date) AS rental_time
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14'
ORDER BY 3 desc;

-- ========================================================================
-- Упражнение 3.1
SELECT actor_id, first_name, last_name
FROM actor
ORDER BY last_name, first_name;

-- Упражнение 3.2
SELECT actor_id, first_name, last_name
FROM actor
WHERE (last_name = 'WILLIAMS') OR (last_name = 'DAVIS');

-- Упражнение 3.3
SELECT DISTINCT customer_id
FROM rental
WHERE date(rental_date) = '2005-06-05';

-- Упражнение 3.4
SELECT c.email, r.return_date
FROM customer AS c
    INNER JOIN rental AS r
    ON c.customer_id = r.customer_id
WHERE date(r.rental_date) = '2005-06-14'
ORDER BY r.return_date desc;

-- ========================================================================
-- ФИЛЬТРАЦИЯ

-- неравенство (!=) тут обозначается <>

-- Удаление строк где срок аренды не 2005 и не 2006
DELETE FROM rental
WHERE year(rental_date) <> 2005 AND year(rental_date) <> 2006;

-- Оператор between для условий диапозона с 2мя границами:
SELECT customer_id, rental_date
FROM rental
WHERE rental_date BETWEEN '2005-06-14' AND '2005-06-15';

SELECT customer_id, payment_date, amount
FROM payment
WHERE amount BETWEEN 10.0 AND 11.99;

-- Есть еще строковые диапозоны
SELECT last_name, first_name
FROM customer
WHERE last_name BETWEEN 'FA' AND 'FR';

-- Вместо того чтобы проверять много OR, можно использовать IN
SELECT title, rating
FROM film
WHERE rating IN ('G', 'PG');

-- ИСПОЛЬЗОВАНИЕ ПОДЗАПРОСОВ
SELECT title, rating
FROM film
WHERE rating IN (
    SELECT rating
    FROM film
    WHERE title LIKE '%PET%'
);

-- Условия соответствия
SELECT last_name, first_name
FROM customer
WHERE left(last_name, 1) = 'Q';

SELECT last_name, first_name
FROM customer
WHERE last_name LIKE '_A_T%S';
-- _ один символ, % сколько угодно символов

-- Использование регулярных выражений
SELECT last_name, first_name
FROM customer
WHERE last_name REGEXP '^[QY]';
