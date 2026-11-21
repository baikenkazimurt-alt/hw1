-- 1. Все сохранённые позиции (проверка, что их минимум 10)
SELECT id, title, price, rating, url
FROM deals
ORDER BY id ASC;

-- 2. Выгодные предложения до £20 по возрастанию цены
SELECT title, price, rating, url
FROM deals
WHERE price <= 20.0
ORDER BY price ASC;

-- 3. Товары с высоким рейтингом (4 и выше)
SELECT title, price, rating, url
FROM deals
WHERE rating >= 4
ORDER BY rating DESC, price ASC;

-- 4. Средняя цена и количество позиций по каждому рейтингу
SELECT rating, COUNT(*) AS total_items, ROUND(AVG(price), 2) AS avg_price
FROM deals
GROUP BY rating
ORDER BY rating DESC;

-- 5. Поиск по части названия
SELECT title, price, rating, url
FROM deals
WHERE title LIKE '%a%'
ORDER BY price ASC;