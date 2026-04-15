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