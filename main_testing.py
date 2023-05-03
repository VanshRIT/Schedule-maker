import mysql.connector
import dbconfig
from tabulate import tabulate

db = mysql.connector.connect(
    host=dbconfig.HOST,
    user=dbconfig.USER,
    password=dbconfig.PASSWORD,
    database=dbconfig.DATABASE
)

c = db.cursor()
c.execute('SELECT * FROM class_updated')
data = c.fetchall()

# get the column names from the cursor description
headers = [col[0] for col in c.description]

# print the data in a tabular format
print(tabulate(data, headers=headers))
