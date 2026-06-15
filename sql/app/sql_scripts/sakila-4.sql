-- =====================================================
-- Подзапросы

SELECT customer_id, first_name, last_name
FROM customer
WHERE customer_id = (SELECT MAX(customer_id) FROM customer);

SELECT city_id, city
FROM city
WHERE country_id <> (
    SELECT country_id FROM country WHERE country = 'India'
);

-- Подзапросы с несколькими строками и одним столбцом
-- Операторы in и not in

SELECT country_id
FROM country
WHERE country IN ('Canada', 'Mexico');

-- |
-- v

SELECT city_id, city
FROM city
WHERE country_id IN (
    SELECT  country_id
    FROM country
    WHERE country IN ('Canada', 'Mexico')
);

-- /

-- SELECT city_id, city
-- FROM city
-- WHERE country_id IN (
--     SELECT  country_id
--     FROM country
--     WHERE country NOT IN ('Canada', 'Mexico')
-- );

-- Оператор ALL

SELECT first_name, last_name
FROM customer 
WHERE customer_id <> ALL (
    SELECT customer_id
    FROM payment
    WHERE amount = 0
);

-- Позволяет сравнивать отдельное значение с каждым значением в наборе

-- Но того же результата можно добиться с помощью NOT IN
-- Это уже дело вкуса

-- SELECT first_name, last_name
-- FROM customer 
-- WHERE customer_id NOT IN (
--     SELECT customer_id
--     FROM payment
--     WHERE amount = 0
-- );

-- !!! ВАЖНО ЧТОБЫ ПО ПРАВУЮ СТОРОНУ <> ALL / NOT IN НЕ БЫЛО NULL !!!

-- Подзапрос в предложении having

-- Все клиенты общее количество прокатов фильмов у которых превышает значение прокатов у любого из североамериканских клиентов
-- (подзапрос = ) Общее кол-во прокатов фильмов для каждого клиента в Северной Америке
SELECT customer_id, count(*)
FROM rental
GROUP BY customer_id
HAVING count(*) > ALL (
    SELECT count(*)
    FROM rental r
        INNER JOIN customer c
        ON r.customer_id = c.customer_id
        INNER JOIN address a
        ON c.address_id = a.address_id
        INNER JOIN city ct
        ON a.city_id = ct.city_id
        INNER JOIN country co
        ON ct.country_id = co.country_id
    WHERE co.country IN ('United States', 'Mexico', 'Canada')
    GROUP BY r.customer_id
);

-- Оператор ANY

-- Все клиенты чьи суммарные платежи за прокат фильмов превышают суммарные платежи всех клиентов в 
-- Боливии, Парагвае, Чили
SELECT customer_id, sum(amount)
FROM payment
GROUP BY customer_id
HAVING sum(amount) > ANY (
    SELECT sum(p.amount)
    FROM payment p
        INNER JOIN customer c
        ON p.customer_id = c.customer_id
        INNER JOIN address a
        ON c.address_id = a.address_id
        INNER JOIN city ct
        ON a.city_id = ct.city_id
        INNER JOIN country co
        ON ct.country_id = co.country_id
    WHERE co.country in ('Bolivia', 'Paraguay', 'Chile')
    GROUP BY co.country
);

-- = ANY - то же самое что и IN

-- Многостолбцовые запросы
SELECT fa.actor_id, fa.film_id
FROM film_actor fa
WHERE fa.actor_id IN 
    (SELECT actor_id FROM actor WHERE last_name = 'MONROE')
    AND
    (SELECT film_id FROM film WHERE rating = 'PG');

-- однако это ^ можно объединить в это:
SELECT actor_id, film_id
FROM film_actor
WHERE (actor_id, film_id) IN (
    SELECT a.actor_id, f.film_id
    FROM actor a
        CROSS JOIN film f
    WHERE a.last_name = 'MONROE' AND f.rating = 'PG'
);

-- Коррелированный запрос - зависит от содержащей его инструкции и выполняется по одному
-- разу для каждой строки-кандидата
-- Из-за чего могут быть проблемы с производительностью
-- Особенно при большом количестве строк в содержащем подзапросе
SELECT c.first_name, c.last_name
FROM customer c 
WHERE 20 = (
    SELECT count(*) FROM rental r 
    WHERE r.customer_id = c.customer_id
);

-- Кроме условий равенства коррелированные подзапросы можно использовать
-- в условиях других типов:
SELECT c.first_name, c.last_name
FROM customer c, 
WHERE (
    SELECT sum(p.amount) FROM peyment p
    WHERE p.customer_id = c.customer_id
) BETWEEN 180 AND 240;

-- Оператор exists
-- наиболее распрастранен для создания условий с коррелированными подзапросами
-- Например нужно определить существование связи безотносительно к количеству.

--  Следующий запрос находит всех клиентов которые взяли напрокат хотя бы 
-- один фильм до 25мая 2005года без учета того сколько фильмов было взято
SELECT c.first_name, c.last_name
FROM customer c
WHERE EXISTS (
    SELECT 1 FROM rental r 
    WHERE r.customer_id = c.customer_id
    AND date(r.rental_date) < '2005-05-25'
);

-- по сути мы можем возвращать тут в подзапросе что угодно, т.к. мы всеравно это никак не используем
-- но всеравно для exists принято select 1 или select *

-- Так же можно использовать not exists

SELECT a.first_name, a.last_name
FROM actor a
WHERE NOT EXISTS (
    SELECT 1
    FROM film_actor fa 
        INNER JOIN film f ON f.film_id = fa.film_id
    WHERE fa.actor_id = a.actor_id
        AND f.rating = 'R'
);

-- Изменение с помощью подзапросов

-- (с проверкой на null)
UPDATE customer c 
SET c.last_update = (
    SELECT max(r.rental_date) FROM rental r 
    WHERE r.customer_id = c.customer_id)
WHERE EXISTS (
    SELECT 1 FROM rental r 
    WHERE r.customer_id = c.customer_id
);

-- ВАЖНО: псевдонимы таблиц при использовании инструкции DELETE могут быть недоступны
-- придется использовать полные названия таблиц


-- =====================================================
-- Подзапросы как источники данных 

SELECT c.first_name, c.last_name, p.num_rentals, p.tot_payments
FROM customer c 
    INNER JOIN (
        SELECT customer_id, count(*) num_rentals, sum(amount) tot_payments
        FROM payment
        GROUP BY customer_id
    ) AS p 
    ON c.customer_id = p.customer_id;

-- Создание данных

SELECT pgroups.name, count(*) num_customers
FROM  (
    SELECT customer_id, count(*) num_rentals, sum(amount) tot_payments
    FROM payment
    GROUP BY customer_id
) AS p 
INNER JOIN (
    SELECT 'Small Fry' name, 0 low_limit, 74.99 high_limit
    UNION ALL
    SELECT 'Average Joes' name, 75 low_limit, 149.99 high_limit
    UNION ALL
    SELECT 'Heavy Hitters' name, 150 low_limit, 9999999.99 high_limit;
) AS pgroups
ON p.tot_payments 
    BETWEEN pgroups.low_limit AND pgroups.high_limit
GROUP BY pgroups.name;

