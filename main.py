import response

lista = ['14-260 Lubawa Matejki 29', '83-323 Gdynia Morska 1/3']
for adres in lista:
    resp = response.lat_lon(adres)
    print(resp['lat'])
    print(resp['lon'])
