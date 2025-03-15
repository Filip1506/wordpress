import mysql.connector

db_config = {
    "host": "mysql30.unoeuro.com",
    "user": "itco_dk",
    "password": "BbawpD64fGFcdAEgrzRt",
    "database": "itco_dk_db_test"
}

try:
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()
    cursor.execute("SHOW TABLES;")
    tables = cursor.fetchall()
    print("Tabeller i databasen:", tables)
except Exception as e:
    print("Databasefejl:", e)
finally:
    cursor.close()
    db.close()