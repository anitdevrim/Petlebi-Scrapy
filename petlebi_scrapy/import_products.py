import json
import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def main():
    # Open the product json file we previously scraped from website
    try:
        with open(os.getenv('json_file_path'), 'r') as json_file:
            data = json.load(json_file)
    except:
        print("Couldn't read json file.")

    # Connect to the database using the credentials coming from .env file
    db_connection = mysql.connector.connect(
        host = os.getenv('host'),  # host_name
        user = os.getenv('username'),  # user_name
        password = os.getenv('pwd'),  # password
        database = os.getenv('database'),  # database_name
    )

    cursor = db_connection.cursor()

    # Open the sql file that will create the MySQL table in our database
    try:
        with open('petlebi_create.sql', 'r') as sql_file:
            create_table_script = sql_file.read()
    except:
        print("Error occured while opening the SQL file.")

    cursor.execute(create_table_script)

    db_connection.commit()  # Commit changes to database

    # Open the sql file that will insert the product values
    try:
        with open('petlebi_insert.sql', 'r') as sql_file:
            insert_table_script = sql_file.read()
    except:
        print("Error occured while opening the SQL file.")

    for product in data:  # For each product in json file
        product_params = (product['product_name'], product['product_id'], product['product_brand'], product['product_price'], product['product_stock'], product['product_category'],product['product_url'], product['product_img'], product['product_barcode'],product['product_description'], product['product_sku'])
        cursor.execute(insert_table_script,product_params)  # Insert the values

    db_connection.commit()  # Commit changes to database
    cursor.close()
    db_connection.close()
    
if __name__ == '__main__':
    main()
