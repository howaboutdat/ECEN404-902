import mysql.connector
import datetime

#Establish database connection
conn = mysql.connector.connect(host="0.tcp.ngrok.io",port="19739", user="root", password="", database="gro_data")

if (conn):
    print("Connection successful")
else:
    print("Connection unsuccessful")

cursor = conn.cursor()


#Append Trash_table within the last 24 hours
current_time = datetime.datetime.now()
start_time = datetime.datetime.now() - datetime.timedelta(3)
cursor.execute("Select * from trash_data WHERE Timestamp BETWEEN %s AND %s ",(start_time,current_time))
trash_table =cursor.fetchall()

print(trash_table) # for visual


#Append Location_table


#Status = 1 means trash is not picked up
#Status = 0 means trash is picked up

def check_sensors(trash_table):
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    for key,timestamp, value1, value2, value3 in trash_table:
        query = "REPLACE INTO loc_data SET  ID_module =%s, Date =%s, Capacity = %s ,Status = %s"
        if(value1 <= 5.0 and value2 <= 5.0 and value3 <= 5.0):
            val = (key, current_date, "Full", "1")
            cursor.execute(query,val)
            conn.commit()
            print(str(key) +": Full")
        elif(value1 <= 5.0 and value2 <= 5.0):
            val = (key, current_date, "Close to full", "1")
            cursor.execute(query,val)
            conn.commit()
            print(str(key) +": Close to full")
        elif(value1 >= 40.0 or value2 >= 40.0 or value3 >= 40.0):
            val = (key, current_date, "Empty", "0")

            cursor.execute(query,val)
            conn.commit()
            print(str(key)+": Empty")

    return 0

check_sensors(trash_table)







conn.commit()
# closing cursor connection
cursor.close()
# closing connection object