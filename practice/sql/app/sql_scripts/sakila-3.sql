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
