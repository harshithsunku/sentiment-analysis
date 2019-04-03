import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="fk"
)

mycursor = mydb.cursor()

sql = "INSERT INTO tv_data (p_id, reviews , score) VALUES (%s, %s , %s)"
val = ("John", "Highway 21" , 21.66)

mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")