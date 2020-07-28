import os
import psycopg2
import sqlite3
from dotenv import load_dotenv
"""
Note to self:


PRIOR TO RUNNING FIRST TIME RUN THIS CODE IN TERMINAL:

                    pip install -U python-dotenv

"""
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")


### Connect to ElephantSQL-hosted PostgreSQL
conn = psycopg2.connect(dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)
### A "cursor", a structure to iterate over db records to perform queries
cur = conn.cursor()
### An example query
cur.execute('SELECT * from test_table;')
### Note - nothing happened yet! We need to actually *fetch* from the cursor
results = cur.fetchall()

print(results)

"""

CONNECT to SQLITE3 DB

"""

sl_conn = sqlite3.connect("rpg_db.sqlite3")
sl_cursor = sl_conn.cursor()
characters = sl_cursor.execute('SELECT * FROM charactercreator_character').fetchall()
print(characters)

"""

Create Character Table in PostGRES

"""

create_character_table_query = '''
CREATE TABLE IF NOT EXISTS rpg_characters (
    character_id SERIAL PRIMARY KEY,
	name VARCHAR(30),
	level INT,
	exp INT,
	hp INT,
	strength INT, 
	intelligence INT,
	dexterity INT,
	wisdom INT
)
'''

cur.execute(create_character_table_query)
conn.commit()

"""

Insert Character Data in POSTGRES

"""
for character in characters:

    insert_query = f''' INSERT INTO rpg_char
        (character_id, name, level, exp, hp, strength, intelligence, dexterity, wisdom) VALUES
        {character}
    '''
    cur.execute(insert_query)

conn.commit()

