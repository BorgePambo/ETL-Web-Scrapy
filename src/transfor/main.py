import pandas as pd
from pathlib import Path
from datetime import datetime
import pyodbc

##file_path = Path('../../data/data.json')

file_path = Path('../../data/my_data.json')

if Path.exists(file_path):
    dframe = pd.read_json(file_path)

    dframe['old_price'] = dframe['old_price'].fillna(0)
    dframe['old_price_cent'] = dframe['old_price_cent'].fillna(0)
    dframe['new_price'] = dframe['new_price'].fillna(0)
    dframe['new_price_cent'] = dframe['new_price_cent'].fillna(0)

    dframe['_old_price'] = dframe['old_price'] + dframe['old_price_cent'] / 100
    dframe['_new_price'] = dframe['new_price'] + dframe['new_price_cent'] / 100

    dframe[ 'review_amount'] = dframe['review_amount'].astype('float64')

    
     # Adding column with data and hour
    dframe['colect_time'] = datetime.now().date()
    dframe['_source'] = "https://lista.mercadolivre.com.br/tenis-corrida-masculino"

    dframe.drop(columns=['old_price', 'old_price_cent', 'new_price', 'new_price_cent'], inplace=True)
    print(dframe.info())


else:
    print('Stop..! The file does not existis.')
    


##Conectando ao banco de dados sql3
import sqlite3

conn = sqlite3.connect('../../data/quotes.db')

dframe.to_sql('mercado_livre_products', conn, if_exists='replace', index=False)

conn.close()


###-----------Abrind o banco de dados sql server ----------------####
connection_data = (
    r"DRIVER={ODBC Driver 17 for SQL Server};"
    r"SERVER=DESKTOP-EO6D9UQ\OLAP1;"
    r"DATABASE=Estudos;"
    r"UID=sa;"
    r"PWD=123456"
)

connection = pyodbc.connect(connection_data)
cursor = connection.cursor()

table_name = 'Products'
columns = ', '.join([
    'name VARCHAR(255)',
    'description TEXT',
    'review_number FLOAT',
    'review_amount FLOAT',
    '_old_price FLOAT',
    '_new_price FLOAT',
    'colect_time DATETIME',
    '_source VARCHAR(255)'
])

create_table_query = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table_name}' AND xtype='U') CREATE TABLE {table_name} ({columns})"
cursor.execute(create_table_query)
connection.commit()

for index, row in dframe.iterrows():
    placeholders = ', '.join(['?' for _ in row])
    insert_query = f"INSERT INTO {table_name} ({', '.join(dframe.columns)}) VALUES ({placeholders})"
    cursor.execute(insert_query, tuple(row))
connection.commit()

cursor.close()
connection.close()
print("Com sucesso")