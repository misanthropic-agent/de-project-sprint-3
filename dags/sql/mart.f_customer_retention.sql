DELETE FROM mart.f_customer_retention WHERE period_id = EXTRACT(WEEK FROM {{ds}}::date)

WITH cte AS (
    SELECT fs.item_id, fs.customer_id, dc.week_of_year as period_id  FROM mart.f_sales fs
    JOIN mart.d_calendar dc ON dc.date_id = fs.date_id
    JOIN
)