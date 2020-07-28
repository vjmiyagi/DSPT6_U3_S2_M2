import os
import psycopg2
import sqlite3
import pandas as pd 
import numpy as np
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


"""

Connect to ElephantSQL-hosted PostgreSQL

"""
conn = psycopg2.connect(dbname=DB_NAME,
                        user=DB_USER,
                        password=DB_PASS,
                        host=DB_HOST)
### A "cursor", a structure to iterate over db records to perform queries
cur = conn.cursor()
### An example query
cur.execute('SELECT * from test_table;')
### Get Results
results = cur.fetchall()
print(results)

# Get Titanic dataset into pandas DataFrame
url = "https://raw.githubusercontent.com/vjmiyagi/DS-Unit-3-Sprint-2-SQL-and-Databases/master/module2-sql-for-analysis/titanic.csv"

df = pd.read_csv(url)
print(df.shape)
print(df.head())
print(df.columns)
df.rename(columns={"Siblings/Spouses Aboard": "SiblingSpousesAboard", "Parents/Children Aboard": "ParentsChildrenAboard"}, inplace=True)
print(df.columns)
df1 = pd.DataFrame()
df1["ID"] = (np.arange(887)) +1

print(df1)

titanic_df = pd.concat([df1, df], axis=1, sort=False)
print(titanic_df)


"""

Create TITANIC Table in PostGRES

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

"""

Create Titanic Table in PostGRES

"""

create_titanic_table_query = '''
CREATE TABLE IF NOT EXISTS titanic (
    ID SERIAL PRIMARY KEY,
    Survived BOOLEAN,
    Pclass INT,
    Name VARCHAR(40),
    Sex VARCHAR(6),
    Age INT,
    SiblingSpousesAboard INT,
    ParentsChildrenAboard INT,
    Fare DECIMAL
)
'''

cur.execute(create_titanic_table_query)
conn.commit()

"""

Insert titanic Data in POSTGRES

"""
for pax in titanic_df:

    insert_query = f''' INSERT INTO titanic
        (ID, Survived, Pclass, Name, Sex, Age, SiblingSpousesAboard, ParentsChildrenAboard, Fare) VALUES
        {pax}
    '''
    cur.execute(insert_query)

conn.commit()