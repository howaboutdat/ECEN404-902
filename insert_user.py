import mysql.connector
import datetime
conn = mysql.connector.connect(host="localhost", user="root", password="", database="gro_data")
if (conn):
    print("Connection successful")
else:
    print("Connection unsuccessful")


id_module = input("What's the ID module of the trash can?")
loc = input("What's the location of the trash can?")
capacity = "Empty"
status = 0
date = str(datetime.datetime.today()).split()[0]
cursor = conn.cursor()
sql = "INSERT INTO loc_data(ID_module, Location, Date, Capacity, Status) VALUES (%s,%s,%s,%s,%s)"
val = (id_module,loc,date,capacity,status)
cursor.execute(sql,val)
conn.commit()