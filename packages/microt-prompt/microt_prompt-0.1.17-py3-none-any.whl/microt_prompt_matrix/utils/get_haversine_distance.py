from math import radians, cos, sin, asin, sqrt

def haversine(loc1, loc2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1 = loc1[1]
    lat1 = loc1[0]
    lon2 = loc2[1]
    lat2 = loc2[0]
    if lat1 > 7:  # already radians
        lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r

if __name__ == "__main__":
    lon1 = -103.548851
    lat1 = 32.0004311
    lon2 = -103.6041946
    lat2 = 33.374939

    print(haversine([lat1, lon1], [lat2, lon2]))