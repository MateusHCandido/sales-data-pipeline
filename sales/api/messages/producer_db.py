import time
import json
import psycopg2
from confluent_kafka import Producer

producer = Producer({'bootstrap.servers': 'localhost:9092'})

def delivery_report(err, msg):
    if err:
        print(f'Erro ao entregar mensagem: {err}')
    else:
        print(f'Mensagem entregue em {msg.topic()} [{msg.partition()}]')

def main():
    conn = psycopg2.connect(
        dbname='sales_db',
        user='user',
        password='password',
        host='localhost'
    )
    cursor = conn.cursor()

    last_id = 0

    while True:
        cursor.execute("SELECT * FROM sales_audit_log WHERE id > %s ORDER BY id", (last_id,))
        rows = cursor.fetchall()

        for row in rows:
            log_id, sale_id, product_id, quantity, price_per_unit, sales_date, status, operation, changed_at = row
            event = {
                "sale_id": sale_id,
                "product_id": product_id,
                "quantity": quantity,
                "price_per_unit": float(price_per_unit),
                "sales_date": sales_date.isoformat(),
                "status": status,
                "operation": operation,
                "changed_at": changed_at.isoformat()
            }

            producer.produce('sales-cdc', json.dumps(event).encode('utf-8'), callback=delivery_report)
            last_id = log_id

        producer.flush()
        time.sleep(5)

if __name__ == '__main__':
    main()
