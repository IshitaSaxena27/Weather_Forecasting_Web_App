import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=12345,
  database="weatherforcast"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT DATABASE()")  # To check the current database
result = mycursor.fetchone()
print("Connected to:", result)
