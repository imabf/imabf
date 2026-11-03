-- Small sample schema used to practise tester data-validation queries.
-- Works in SQLite, MySQL (minor syntax tweaks) and Oracle (see notes in checks file).
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;

CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    name        TEXT,
    email       TEXT,
    created_at  TEXT
);
CREATE TABLE orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id INTEGER,
    status      TEXT,
    total       REAL,
    order_date  TEXT
);
CREATE TABLE order_items (
    item_id    INTEGER PRIMARY KEY,
    order_id   INTEGER,
    product    TEXT,
    quantity   INTEGER,
    unit_price REAL
);

-- Sample data with deliberate defects for the checks to find.
INSERT INTO customers VALUES
 (1,'Alice','alice@example.com','2026-01-05'),
 (2,'Bob','bob@example.com','2026-01-06'),
 (3,'Bob','bob@example.com','2026-01-07'),   -- duplicate email
 (4,'Dina',NULL,'2026-01-08');               -- missing email
INSERT INTO orders VALUES
 (100,1,'PAID',50.0,'2026-02-01'),
 (101,2,'PAID',30.0,'2026-02-02'),
 (102,99,'PAID',20.0,'2026-02-03'),          -- orphan: customer 99 does not exist
 (103,1,'SHIPPED',70.0,'2026-02-04');        -- total does not match its items
INSERT INTO order_items VALUES
 (1,100,'Keyboard',1,50.0),
 (2,101,'Mouse',2,15.0),
 (3,102,'Cable',1,20.0),
 (4,103,'Monitor',1,60.0),
 (5,999,'Ghost item',1,5.0),                 -- orphan: order 999 does not exist
 (6,100,'Mouse pad',-1,5.0);                 -- invalid quantity
