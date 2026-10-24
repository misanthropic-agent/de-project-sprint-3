CREATE TABLE IF NOT EXISTS mart.f_customer_retention (
    new_customers_count INT,
    returning_customers_count INT,
    refunded_customers_count INT,
    period_name VARCHAR(10),
    period_id INT,
    item_id INT,
    new_customers_revenue NUMERIC,
    returning_customers_revenue NUMERIC,
    customers_refunded INT
);