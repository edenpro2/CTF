import hashlib

hash_lat = "d8fde39f832a41187bf9fd109b0c74c1"
hash_lon = "9a745c279c8a2b3e5c1abf0edddb8e80"

lat = ""
lon = ""

def HashLatLon(l, r, hash:str, acc:int):    
    for i in range(l, r+1):
        for j in range(10**acc):
            degree = f'{i}.{j}' 
            if hashlib.md5(degree.encode()).hexdigest() == hash:
                return degree

print("Comparing lat")
print(HashLatLon(40, 40, hash_lat, 6))
print("Comparing lon")
print(HashLatLon(-74, -73, hash_lon, 6))
