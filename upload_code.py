import serial
import mysql.connector
import time

# open a cursor to the database
conn = mysql.connector.connect(host="0.tcp.ngrok.io",port="19739", user="root", password="", database="gro_data")
cursor = conn.cursor()


#Connect to corresponding COM in computer
device = 'COM5'
try:
    print("Trying...", device)
    arduino = serial.Serial(port = device, baudrate=115200, timeout = 1)
except:
    print("Failed to connect on", device)
    quit()

while True:
    try:
        time.sleep(0.1)
        data = arduino.readline()  # read the data from the arduino
        datastripped = data.decode().strip().split("%")   # split the data by the %
        pieces =[num for num in datastripped if num.isdigit()]
        empty_list=[]
        try:
            if((pieces != empty_list)):
                print(pieces)
                cursor.execute("INSERT INTO trash_data (ID_module, Sensor1, Sensor2, Sensor3) VALUES (%s, %s, %s, %s)", (pieces[0], pieces[1],pieces[2],pieces[3]))
                conn.commit()  # commit the insert

        except mysql.connector.IntegrityError as err:
            print("Failed to insert data to database")
            quit()
    except:
        print('Failed to receive data from sensors')


cursor.close()  # close the cursor



