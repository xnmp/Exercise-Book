#housekeeping
import sys
sys.path.append('/usr/lib/python2.7/dist-packages/')
sys.path.append('/home/chong/anaconda2/lib/python2.7/site-packages')
import sqlite3
import pandas as pd
from sqlalchemy import create_engine
sqlite_db = 'test_db.sqlite'
conn = sqlite3.connect(sqlite_db)
c = conn.cursor()


#make a table and insert some entries

# c.execute('CREATE TABLE houses (field1 INTEGER PRIMARY KEY, sqft INTEGER, bdrms INTEGER, age INTEGER, price INTEGER);')

# last_sale = (None, 4000, 5, 22, 619000)
# c.execute('INSERT INTO houses VALUES (?,?,?,?,?)',last_sale)

# recent_sales = [
#   (None, 2390, 4, 34, 319000),
#   (None, 1870, 3, 14, 289000),
#   (None, 1505, 3, 90, 269000),
# ]
# c.executemany('INSERT INTO houses VALUES (?, ?, ?, ?, ?)', recent_sales)


#load csv into sql
# data = pd.read_csv('housing-data.csv', low_memory=False)
# data.to_sql('houses_pandas',
#             con=conn,
#             if_exists='replace',
#             index=False)

# conn.commit()


#now query
# from pandas.io import sql
# res = sql.read_sql('select * from houses_pandas limit 10', con=conn)
# results = c.execute("SELECT * FROM houses WHERE bdrms = 4")

#sqlalchemy

connect_param = 'postgresql://dsi_student:gastudents@dsi.c20gkj5cvu3l.us-east-1.rds.amazonaws.com:5432/titanic'
engine = create_engine(connect_param)
print pd.read_sql("SELECT * FROM pg_catalog.pg_tables WHERE schemaname='public'", con=engine)
