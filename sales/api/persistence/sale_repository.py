from datetime import datetime
import psycopg2 as psy



class SaleRepository:
    def __init__(self, db_config: dict):
        self.db_config = db_config  

    def __execute_query(self, query, values, fetch=False):
        try:
            connection = psy.connect(**self.db_config)
            cursor = connection.cursor()
            cursor.execute(query, values)
            if fetch:
                result = cursor.fetchall()
            connection.commit()
            cursor.close()
            connection.close()
            return result if fetch else None
        except psy.Error as error:
            print(f'Database error: {error}')
            raise

    def _save_sale(self, sale):
        query = '''
            INSERT INTO oltp.sales (product_id, quantity, price_per_unit, sales_date, status)
            VALUES(%s, %s, %s, %s, %s)
        '''
        values = (
            sale.product_id,
            sale.quantity,
            sale.price_per_unit,
            sale.sales_date,
            sale.status.value
        )
    
        self.__execute_query(query, values)
    
    def _update_sale(self, sale_id):
        query = '''UPDATE oltp.sales SET status = %s WHERE sale_id = %s'''
        values = ('CANCELED', sale_id)

        self.__execute_query(query, values)



