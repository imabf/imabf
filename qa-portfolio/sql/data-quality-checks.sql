-- Tester data-validation queries. Each one should return ZERO rows when data is healthy.
-- Run after schema.sql. Tested on SQLite.

-- 1. Duplicate records (same email used by more than one customer)
SELECT email, COUNT(*) AS occurrences
FROM customers
WHERE email IS NOT NULL
GROUP BY email
HAVING COUNT(*) > 1;

-- 2. NULL / missing mandatory values
SELECT customer_id, name FROM customers WHERE email IS NULL OR TRIM(email) = '';

-- 3. Orphan records: orders whose customer does not exist
SELECT o.order_id, o.customer_id
FROM orders o
LEFT JOIN customers c ON c.customer_id = o.customer_id
WHERE c.customer_id IS NULL;

-- 4. Orphan records: order items whose order does not exist
SELECT i.item_id, i.order_id
FROM order_items i
LEFT JOIN orders o ON o.order_id = i.order_id
WHERE o.order_id IS NULL;

-- 5. Invalid values (quantity or price must be positive)
SELECT item_id, quantity, unit_price
FROM order_items
WHERE quantity <= 0 OR unit_price <= 0;

-- 6. Calculation check: order total must equal the sum of its items
SELECT o.order_id, o.total AS stored_total, SUM(i.quantity * i.unit_price) AS calculated_total
FROM orders o
JOIN order_items i ON i.order_id = o.order_id
GROUP BY o.order_id, o.total
HAVING ROUND(o.total, 2) <> ROUND(SUM(i.quantity * i.unit_price), 2);

-- 7. Count check (reconciliation): compare row counts between source and target
SELECT (SELECT COUNT(*) FROM orders)      AS orders_rows,
       (SELECT COUNT(DISTINCT order_id) FROM order_items) AS orders_with_items;

-- 8. Status values must be from the allowed list
SELECT order_id, status
FROM orders
WHERE status NOT IN ('NEW','PAID','SHIPPED','CANCELLED');

-- Notes for other databases:
--   MySQL : works as is (TEXT dates can be DATE).
--   Oracle: replace TRIM(email) = '' with email IS NULL (Oracle treats '' as NULL).
