import urllib.request, json
#import data about status of whether the trash can is being picked up or not
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", password="", database="gro_data")
if (conn):
    print("Connection successful")
else:
    print("Connection unsuccessful")

cursor = conn.cursor()


from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="my_user_agent")
loc = geolocator.geocode("430 Forest Dr, College Station, TX 77840")
print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)