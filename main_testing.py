import mysql.connector
import dbconfig


db = mysql.connector.connect(
    host=dbconfig.HOST,
    user=dbconfig.USER,
    password=dbconfig.PASSWORD,
    database=dbconfig.DATABASE
)

c = db.cursor()
c.execute("SELECT distinct Subject, Cat from class_updated where sect like \"%L%\"")
data = c.fetchall()
print(data)
print(type(data))