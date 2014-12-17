from geopy import geocoders
import csv

# initialize geopy's geocoder object for Google Maps API v.3
g = geocoders.GoogleV3()

# open data file of Costco addresses
costcos = csv.reader(open('costcos-limited.csv'), delimiter=',')
next(costcos) # skip header in file

# create export file to store Costco GPS coordinates
outfile = open('geocoded.csv', "wb")
writer = csv.writer(outfile, delimiter=",")
header = ["Warehouse Number","Address","City","State","Zip Code","Lat","Lng"]
writer.writerow(header)

# print header
print ("ID,Address,City,State,Zip Code,Latitude,Longitude")

# geocode each address in data file
for row in costcos:
    full_address = row[1] + "," + row[2] + "," + row[3] + "," + row[4]
    try: 
        place, (lat, lng) = list(g.geocode(full_address, exactly_one=False))[0]
        outrow = [row[0], row[1], row[2], row[3], row[4], str(lat), str(lng)]
        writer.writerow(outrow)
        print row[0] + "," + full_address + "," + str(lat) + "," + str(lng)
    except:
        outrow = [row[0], row[1], row[2], row[3], row[4], str(lat), str(lng)]
        writer.writerow(outrow)
        print row[0] + "," + full_address + ",NULL,NULL"

outfile.close()
