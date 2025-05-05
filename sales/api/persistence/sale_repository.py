from fastapi import HTTPException
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
            if cursor.rowcount == 0:
                raise HTTPException(f"Nenhuma venda com ID {values[0]} foi encontrada.")
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
    
    def _cancel_sale(self, sale_id):
        query = '''UPDATE oltp.sales SET status = %s WHERE sale_id = %s'''
        values = ('CANCELED', sale_id)

        self.__execute_query(query, values)

    def _find_sale(self, sale_id):
        query = '''SELECT * FROM oltp.sales WHERE sale_Id = %s'''
        values= (sale_id)

        self.__execute_query(query, values, fetch=True)


_db_config = {
    "dbname": "sales_db",
    "user": "user",
    "password": "password",
    "host": "localhost",
    "port": 5432
}

sales_repository = SaleRepository(_db_config)