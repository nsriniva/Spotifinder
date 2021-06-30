import pandas as pd
import psycopg2
from psycopg2.extensions import register_adapter, AsIs
from IPython.display import display
import numpy as np
from numpy import int64
from decouple import config
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
pd.set_option('display.max_columns', 14)
df = pd.read_csv('../data/NLP_songs_data.zip')
# df.drop(columns=['lyrics'], inplace=True)
column_names = list(df.columns)
print(column_names)
display(df.head())
# print(df.columns)
# print([dt.name[:-2] for dt in df.dtypes])
# breakpoint()
cols = list(df.columns)
# print(cols)
data_types = [dt.name for dt in df.dtypes]
for n, i in enumerate(data_types):
    if i == "int64":
        data_types[n] = "int"
for n, i in enumerate(data_types):
    if i == "object":
        data_types[n] = "text"
print(data_types)
assert len(cols) == len(data_types)
baseQuery = "CREATE TABLE NLP_songs_data (\n"
for idx, col in enumerate(zip(cols, data_types)):
    if idx == len(cols) - 1:
        baseQuery += col[0] + " " + col[1] + ");"
    else:
        baseQuery += col[0] + " " + col[1] + ",\n"
baseInsertQuery = "INSERT INTO NLP_songs_data ("
for idx, col in enumerate(cols):
    if idx == len(cols) - 1:
        baseInsertQuery += col + ") VALUES "
    else:
        baseInsertQuery += col + ", "
# baseQuery += ');'
print(baseQuery)
conn = psycopg2.connect(
     database=config('DB_NAME'),
     user=config('DB_USER'),
     password=config('DB_PASS'),
     host=config('DB_HOST')
)
curs = conn.cursor()
curs.execute(baseQuery)
# print(conn)
data = df.to_records(index=False)
# curs.executemany(insertQuery, data)
for row in data:
    curs.execute(baseInsertQuery + str(row))
conn.commit()
conn.close()

