import response
import distance

lista = ['14-260 Lubawa Matejki 29', '83-323 Gdynia Morska 1/3']
lat2 = 52.231748
lon2 = 21.006056

for adres in lista:
    resp = response.lat_lon(adres)
    lat1 = resp['lat']
    lon1 = resp['lon']
    print(lat1,lon1,lat2,lon2)
    dist = distance.distance(lat1,lon1,lat2,lon2)
    print(dist)
