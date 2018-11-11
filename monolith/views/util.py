#utility file

#convert from secons to meter
def sec2minsec(seconds):
    minutes = seconds // 60
    seconds = ((seconds / 60 ) - minutes) * 60

    return minutes, seconds

#convert from meters to km
def m2km(dist):
    return dist/1000

#convert from km to meter
def km2m(dist):
    return dist*1000

#convert from m/h to km/h
def mh2kmh(speed):
    return speed*3.6