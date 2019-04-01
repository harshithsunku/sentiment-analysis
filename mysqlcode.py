import mysql.connector
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  database="fk"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT p_id,p_productUrl FROM mobiles")
myresult = mycursor.fetchall()
for x in range(10):
  print(myresult[x][1])
