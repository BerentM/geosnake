# http://www.movable-type.co.uk/scripts/latlong.html
import math

def distance(lat1, lon1, lat2, lon2):
    """Funkcja zwraca odległość pomiędzy dwoma punktami w kilometrach.
    Odległość liczona jest w prostej lini między dwoma pkt."""
    EARTH_RADIUS = 6378137
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = (math.sin(dLat/2) * math.sin(dLat/2) + 
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dLon/2) * math.sin(dLon/2))
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = round(((EARTH_RADIUS * b)/1000), 3)

    return dist 
 
def distanceMeter(lat1, lon1, lat2, lon2):
    """Funkcja zwraca odległość pomiędzy dwoma punktami w metrach.
    Odległość liczona jest w prostej lini między dwoma pkt."""
    EARTH_RADIUS = 6378137
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)

    a = (math.sin(dLat/2) * math.sin(dLat/2) + 
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
            math.sin(dLon/2) * math.sin(dLon/2))
    b = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist = EARTH_RADIUS * b

    return dist 
    
if __name__ == '__main__':
    lat1 = 53.50713585
    lon1 = 19.7379455215222
    lat2 = 54.5189486
    lon2 = 18.5295708994249
    print(distance(lat1,lon1,lat2,lon2))
