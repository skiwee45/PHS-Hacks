import requests
import pandas as pd
import csv
from geopy.geocoders import GoogleV3
import geopy.distance
import googlemaps
from pymongo import MongoClient
import json
from io import StringIO 
API = 'AIzaSyC1COUUe3Uhkj06qQo-_Ha2HwABlyB7qq4'

params = {
  "api_key": "tvJnAVHJT6Tc",
  "format": "csv"
}
r = requests.get('https://parsehub.com/api/v2/projects/tY5vNNb-Yx5n/last_ready_run/data', params=params)
CMDATA = StringIO(r.text)

geolocator = GoogleV3(api_key=API)

#finish adding lat and long to csv using pandas and geocoding api, then push to mongodb
#https://pyshark.com/geocoding-in-python/#:~:text=%20Geocoding%20addresses%20and%20locations%20in%20Python%20,own%20class.%20%20...%20Now%20we...%20More%20

#open the file in text mode
#read the CSV file

data = pd.read_csv(CMDATA, sep=",")

#print the result
data['cm_weekOfDate'] = pd.to_datetime(data.cm_weekOfDate)
data['cm_weekOfDate'] = data['cm_weekOfDate'].dt.strftime('%m/%d/%Y')
print(data)
data['address'] = ""
data['latitude'] = ""
data['longitude'] = ""

from geopy import geocoders
from geopy.exc import GeocoderTimedOut
for i in data.index:
  name = data.loc[i,'cm_name'] + data.loc[i,'cm_state']
  #print(1)
  try:
    location = geolocator.geocode(name, timeout=10)
    #fix for when geocode cannot find address
    data.loc[i,'address'] = location.address
    data.loc[i,'latitude'] = location.latitude
    data.loc[i,'longitude'] = location.longitude
  except AttributeError:
    data.loc[i,'address'] =""
    data.loc[i,'address'] =""
    data.loc[i,'address'] =""
print(data)

# Connect to MongoDB

client =  MongoClient("mongodb+srv://climap:F31C7F@usareportedwildfires.mtw64.mongodb.net/climap?retryWrites=true&w=majority")
db = client['Climap']
collection = db['USAWildfiresReported']
#collection.insert_many(data)
data_json = json.loads(data.to_json(orient='records'))
collection.insert_many(data_json)





''' 
geolocator = GoogleV3(api_key=API)

print(type(geolocator))

name = 'Empire State Building' 
location = geolocator.geocode(name)

print(location.address)
print(location.latitude, location.longitude)

first_location = pd.DataFrame([[name, location.address, location.latitude, location.longitude]],
            columns=['name', 'address', 'lat', 'lon'])

print(first_location)

name = 'Marea Restaurant New York' 
location = geolocator.geocode(name)

second_location = pd.DataFrame([[name, location.address, location.latitude, location.longitude]],
            columns=['name', 'address', 'lat', 'lon'])

my_locations = pd.concat([first_location, second_location], ignore_index=True)

print(my_locations)

'''