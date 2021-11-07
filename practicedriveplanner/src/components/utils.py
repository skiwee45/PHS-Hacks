from math import cos, sin, asin, sqrt, pi,radians
import requests
import pandas as pd
import time
apiKey = "AIzaSyBdZ8GXm2rC-co5WIseA-9sQRtCZATT84I"

data = pd.read_csv('US_Accidents_Dec20_updated.csv')

crashCoords = data[['Start_Lat','Start_Lng','Severity']]
dT = [[(51.4293305,-0.468993), (51.4341449,-0.4673395), (51.4316448,-0.4586662), (51.4306428,-0.4563351), (51.4359898,-0.457517), (51.4656066,-0.4268624),
 (51.4355062,-0.4734752), (51.4439083,-0.4723087), (51.4482983,-0.481203)], [(51.4293305,-0.468993), (51.4227512,-0.448431), (51.4418009,-0.4805363),(51.4268534,-0.4851219), (51.423152,-0.4514907), (51.1509322,0.8692839), (51.4268534,-0.4851219), (51.4338733,-0.4784762), (51.4163822,-0.4747933) ], 
 [(51.4341449,-0.4673395), (51.4347177,-0.4608943), (51.4361685,-0.4584949), (51.4382282,-0.4585683), (51.4350467,-0.4508204), (51.4306428,-0.4563351)]]


"""Geeks4Geeks"""
def get_distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
      
    # calculate the result
    return(c * r)

def getPlaces(radius: int, results: int, xCoord: int, yCoord: int) -> dict:

    radius*=1609

    # requires results % 20 == 0

    request = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={xCoord},{yCoord}&radius={radius}&key={apiKey}" 
    
    currentResults = 0

    results = []
    
    while currentResults != results:
        response = requests.get(request).json()
        if "next_page_token" not in response:
            break
        results.extend([*map(lambda x: x['geometry']['location'],response['results'])])
        nextPageToken = response['next_page_token']
        request = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={nextPageToken}&key={apiKey}"
        currentResults+=20
        time.sleep(2)
    return results
def getDirections(sxCoord: int, syCoord: int, exCoord: int, eyCoord: int):
    url = f"https://maps.googleapis.com/maps/api/directions/json?origin={sxCoord},{syCoord}&destination={exCoord},{eyCoord}&key={apiKey}"
    return [*map(lambda x: x['end_location'], requests.get(url).json()['routes'][0]['legs'][0]['steps'])]
def getCoordinatesAlongPath(sxCoord: int, syCoord: int, coords):
    paths = []
    for coord in coords:
        currentPath = []  
        currentPath.extend(getDirections(sxCoord, syCoord, coord['lat'], coord['lng']))
        #currentPath.extend(getDirections(coord['lat'], coord['lng'], sxCoord, syCoord))

        paths.append(currentPath)
    return paths
def getPathCoordinates(sxCoord: int, syCoord: int, radius: int):
    possibleCords = getPlaces(radius, 20, sxCoord, syCoord)[:5]
    return getCoordinatesAlongPath(sxCoord, syCoord, possibleCords)
def compute_gmaps_distance(xlat, xlong, ylat, ylong):
     url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={xlat},{xlong}&destinations={ylat},{ylong}&key={apiKey}"
     response = requests.get(url)
     return response.json()['rows'][0]['elements'][0]['distance']['value']
def getTrafficInfoSingle(xCoord, yCoord):
    url = f"https://traffic.ls.hereapi.com/traffic/6.1/flow.json?bbox={xCoord},{yCoord};{xCoord + 0.0001},{yCoord + 0.0001}&apiKey=62S2EjFhKZy8jxtFhGkWTI5F725CclbJrpaFXiRd9UY"
    response =  requests.get(url).json()
    JF = 0
    n = 0
    try:
        for data in response['RWS'][0]['RW']:
            JF+=data['FIS'][0]['FI'][0]['CF'][0]['JF']
            n+=1
    except Exception:
        return 0

    return JF/n
def compute_total_crashes(x1, y1):
    totalCrashes = 0
    for crashCoord in crashCoords.itertuples():
        if (abs(x1 - crashCoord.Start_Lat) < 0.01 or abs(y1 - crashCoord.Start_Lng) < 0.01):
            if get_distance(x1, crashCoord.Start_Lat, y1, crashCoord.Start_Lng) <= 5:
                totalCrashes+=1
    return totalCrashes
def getSinuodalValue(paths, n = 5):
    sinuodal_value = []
    for path in paths[:n]:
        mid = len(path) // 2
        a = get_distance(path[0]['lat'], path[mid]['lat'], path[0]['lng'], path[mid]['lat'])
        b = compute_gmaps_distance(path[0]['lat'], path[0]['lng'], path[mid]['lat'], path[mid]['lng'])


        d = compute_gmaps_distance(path[mid]['lat'], path[mid]['lng'], path[0]['lat'], path[0]['lng'])

        sinuodal_value.append((b/a + d/a) * 1/2)

    return sinuodal_value

def getTotalCrashes(paths, n = 5):
    computed = 0
    totalCrashes = []
    for path in paths[:n]:
        crashes = 0
        for coord in path:
            crashes+=compute_total_crashes(coord['lat'], coord['lng'])
        computed+=1
        totalCrashes.append(crashes)
    return totalCrashes
def getTraffic(paths, n = 5):
    jf_ = []
    for path in paths[:n]:
        totalJF = 0
        n = 0
        for coord in path:
            totalJF+=getTrafficInfoSingle(coord['lat'], coord['lng'])
            n+=1
        jf_.append(totalJF/n)
    return jf_
def pathSinuodalValue(path):
    values = []
    for x in range(len(path)):
        if x + 1 < len(path):
            values.append(getSinuodalValue([[{ 'lat': path[x][0], 'lng': path[x][1]}, {'lat':path[x+1][0], 'lng': path[x+1][1]}]]))
    return values
def euclidean_distance(x1, x2):
    s = 0
    for x in range(len(x1)):
        s+=(x1[x] - x2[x]) ** 2
    return s ** 0.5
def compute_ed_from_acc(paths):
    eDistance = []
    for path in paths:
        drivingPath = pathSinuodalValue(dT[1][:len(path)])[0]
        our_path_sin = pathSinuodalValue(path)[0]
        eDistance.append(euclidean_distance(drivingPath, our_path_sin))
    return eDistance

def loss(margin=1):
    # Contrastive loss = mean( (1-true_value) * square(prediction) +
    #                         true_value * square( max(margin-prediction, 0) ))
    def contrastive_loss(y_true, y_pred):

        square_pred = tf.math.square(y_pred)
        margin_square = tf.math.square(tf.math.maximum(margin - (y_pred), 0))
        return tf.math.reduce_mean(
            (1 - y_true) * square_pred + (y_true) * margin_square
        )

    return contrastive_loss


