import requests

adres = '80-350'
raw_request = requests.get("https://nominatim.openstreetmap.org" \
        "/?format=json&addressdetails=1&q={}&format=json&limit=1").format(adres)

print(raw_request)
