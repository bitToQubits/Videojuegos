import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="Rage"
)

mycursor = mydb.cursor()

ID_Jugador = "00725217"
nombre = "Johann"
Apellido = "Lewis"
edad = 15
cultura = "Guyana"
Puntuacion = 3000

sql = "INSERT INTO Jugadores (ID_Jugador, nombre, Apellido,  edad, cultura, Puntuacion)" \
      " VALUES (00725217, Johann, Lewis, 15, Guyana, 3000)"
val = (ID_Jugador, nombre, Apellido, edad, cultura,Puntuacion)
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "fila insertada.")
