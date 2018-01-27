import requests
import time

def lat_lon(*args):
    """Funkcja jako argumenty przyjmuje poszczegolne elementy adresu"""
    adr = ""
    for arg in args:
        adr = adr+"+"+arg.replace(' ','+').replace(',','')
    adres = adr[1:]

    time.sleep(1.5)
    response = requests.get("https://nominatim.openstreetmap.org" \
            "/?format=json&addressdetails=1&q={}&format=json&limit=1".format(adres))

    data = response.json()[0]
    # Zwraca szerokosc i dlugosc geograficzna
    # latwo mozna ja przerobic aby zwracala inne elementy
    return {'lat':data['lat'], 'lon':data['lon']}

if __name__ == '__main__':
    resp = lat_lon('83-323', 'Gdynia Morska', '1/3')
    print(resp['lat'])
    print(resp['lon'])
