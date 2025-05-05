-- Table log
CREATE TABLE oltp.sales_audit_log (
    id SERIAL PRIMARY KEY,
    sale_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    price_per_unit NUMERIC,
    sales_date TIMESTAMP,
    status VARCHAR,
    operation VARCHAR, -- INSERT, UPDATE, DELETE
    changed_at TIMESTAMP DEFAULT NOW()
);

-- Function for changes record  
CREATE OR REPLACE FUNCTION oltp.log_sales_changes()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO oltp.sales_audit_log (sale_id, product_id, quantity, price_per_unit, sales_date, status, operation)
        VALUES (NEW.sale_id, NEW.product_id, NEW.quantity, NEW.price_per_unit, NEW.sales_date, NEW.status, 'INSERT');
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO oltp.sales_audit_log (sale_id, product_id, quantity, price_per_unit, sales_date, status, operation)
        VALUES (NEW.sale_id, NEW.product_id, NEW.quantity, NEW.price_per_unit, NEW.sales_date, NEW.status, 'UPDATE');
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO oltp.sales_audit_log (sale_id, product_id, quantity, price_per_unit, sales_date, status, operation)
        VALUES (OLD.sale_id, OLD.product_id, OLD.quantity, OLD.price_per_unit, OLD.sales_date, OLD.status, 'DELETE');
        RETURN OLD;
    END IF;
END;
$$ LANGUAGE plpgsql;

-- Trigger for sales table
CREATE TRIGGER trg_sales_cdc
AFTER INSERT OR UPDATE OR DELETE ON oltp.sales
FOR EACH ROW EXECUTE FUNCTION oltp.log_sales_changes();
