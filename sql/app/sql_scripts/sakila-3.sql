-- группировка и агрегация

-- концепции группировки

-- представим что я управляю отправкой купонов на бесплатную аренду по адресам 
-- лучших клиентов 
-- select customer_id from rental;

-- по этому запросу где 600 клиентов и 16к записей - невозможно определить какие
-- клиенты взяли напрокат больше всего фильмов. но я могу попросить сгруппировать данные
-- с помощью предложения group

-- select customer_id
-- from rental 
-- group by customer_id;

-- используем агрегатную функцию count(*) для подсчета строк в каждой группе

-- select customer_id, count(*)
-- from rental
-- group by customer_id;

-- осталось сортировать по крутости

SELECT customer_id, count(*)
FROM rental
GROUP BY customer_id
HAVING COUNT(*) >= 40
ORDER BY 2 DESC;

-- мы не можем обратиться к count() перед order by в предложении where
-- это вызвало бы ошибку т.к. группы еще не были сформированны
-- вместо этого условия групп помещаются в предложение having

--   ====================================================== 

-- агрегатные функции

-- max()
-- min()
-- avg()
-- sum()
-- count()

-- Запрос в котором используются все распрастраненные агрегатные функции
SELECT customer_id, 
    MAX(amount) AS max_amt,
    MIN(amount) AS min_amt,
    AVG(amount) AS avg_amt,
    SUM(amount) AS tot_amt,
    COUNT(*) AS num_payments
FROM payment
GROUP BY customer_id;

-- Подсчет различных значений
SELECT COUNT(customer_id) AS num_rows,
    COUNT(DISTINCT customer_id) AS num_customers
FROM payment;

-- Использование выражений
SELECT MAX(datediff(return_date, rental_date))
FROM rental;

-- Обработка значений null
CREATE TABLE number_tbl
(val SMALLINT);

INSERT INTO number_tbl
VALUES (1);

INSERT INTO number_tbl
VALUES (3);

INSERT INTO number_tbl
VALUES (5);

SELECT COUNT(*) num_rows,
    COUNT(val) num_vals,
    SUM(val) total,
    MAX(val) max_val,
    AVG(val) avg_val
FROM number_tbl;

INSERT INTO number_tbl
VALUES (NULL);

SELECT COUNT(*) num_rows,
    COUNT(val) num_vals,
    SUM(val) total,
    MAX(val) max_val,
    AVG(val) avg_val
FROM number_tbl;

-- Даже при NULL мы получаем те же значения что и изначально
-- Т.Е. эти функции игнорируют все встречающиеся NULL

-- Группировка по одному столбцу
SELECT actor_id, count(*)
FROM film_actor
GROUP BY actor_id;

-- Многостолбцовая группировка
SELECT fa.actor_id, f.rating, count(*)
FROM film_actor fa
    INNER JOIN film f
    ON fa.film_id = f.film_id
GROUP BY fa.actor_id, f.rating
ORDER BY 1, 2;

-- Группировка с помощью выражений
SELECT extract(YEAR FROM rental_date) year,
    COUNT(*) how_many
FROM rental
GROUP BY extract(YEAR FROM rental_date);

-- Генерация итоговых данных
-- SELECT fa.actor_id, f.rating, count(*)
-- FROM film_actor fa
--     INNER JOIN film f
--     ON fa.film_id = f.film_id
-- GROUP BY fa.actor_id, f.rating WITH ROLLUP
-- ORDER BY 1, 2;

-- Условия группового фильтра
SELECT fa.actor_id, f.rating, count(*) 
FROM film_actor fa
    INNER JOIN film f
    ON fa.film_id = f.film_id
WHERE f.rating IN ('G', 'PG')
GROUP BY fa.actor_id, f.rating
HAVING count(*) > 9;
-- Тут фильтр where действует на данные ДО группировки
-- А having на данные после

-- Упражнение 8.1
SELECT count(*)
FROM payment;

-- Упражнение 8.2
SELECT customer_id, count(*)
FROM payment
GROUP BY customer_id;

-- Упражнение 8.3
SELECT customer_id, count(*)
FROM payment
GROUP BY customer_id
HAVING count(*) > 39;
