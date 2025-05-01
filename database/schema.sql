CREATE SCHEMA IF NOT EXISTS oltp

CREATE TABLE IF NOT EXISTS oltp.sales(
    sale_id INT PRIMARY KEY,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price_per_unit DECIMAL(10,2) NOT NULL,
    sales_date TIMESTAMP NOT NULL,
    status VARCHAR(10) NOT NULL
);