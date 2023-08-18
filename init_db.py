import os
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="flask_db",
    user="postgres",
    password="123"
)

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
            'userid integer NOT NULL,'
            'name varchar (50) NOT NULL,'
            'age integer NOT NULL,'
            'password varchar(50) NOT NULL,'
            'email varchar(50) NOT NULL,'
            'date_register date DEFAULT CURRENT_TIMESTAMP);'
            )

conn.commit()

cur.close()
conn.close()
