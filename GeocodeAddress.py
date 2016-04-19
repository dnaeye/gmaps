# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 07:00:36 2016

GeocodeAddress retrieves the postal code for addresses using the Google Maps Geocoding API.
https://developers.google.com/maps/documentation/geocoding/

Note: Free API requests are limited to 2,500 per day. 
See https://developers.google.com/maps/documentation/geocoding/usage-limits
for more info.

@author: dhong
"""

# import relevant python modules
import csv, time, re, googlemaps

gmaps = googlemaps.Client(key='ENTER_UNIQUE_API_KEY')

# import data file of store addresses
with open(r"D:\Users\dhong\Documents\Code\Python\addresses in.csv","r") as infile:
    reader = csv.DictReader(infile, delimiter=',')
    
    # create output file for trip data via Google Maps API
    outfile = open(r"D:\Users\dhong\Documents\Code\Python\addresses out.csv","wb")
    writer = csv.DictWriter(outfile, fieldnames=['Customer Num','Company','Shipping Address','City','State','Postal Code','County','Latitude','Longitude','Partial Match'], delimiter=',')
    writer.writeheader()

    # initialize temporary postal code variables
    postal_code_base = ''
    postal_code_suffix = ''
    county = ''

    # loop through each store in import file to retrieve geocode data from Google    
    for row in reader:
        
        # identify portion of shipping address that is relevant for geocoding
        street_address_length = len(row['Shipping Address'])
        street_address_number = re.search('\d',row['Shipping Address'])
        
        # find index of street address number; if none, start at 0
        try:
            street_address_number = street_address_number.start()
        except:
            street_address_number = 0
            
        # create cleaned shipping address
        row['Shipping Address'] = row['Shipping Address'][street_address_number:street_address_length].title()
        
        # call Google Maps API Geocode function
        address = row['Shipping Address'] + ',' + row['City'] + ',' + row['State']
        
        try:        
            result = gmaps.geocode(address)
        
            # loop through JSON to find city, county, postal code data
            for dct in result[0]['address_components']:
                if dct['types'][0] == 'administrative_area_level_2':
                    county = dct['long_name']
                if dct['types'][0] == 'postal_code':
                    postal_code_base = dct['long_name']
                if dct['types'][0] == 'postal_code_suffix':
                    postal_code_suffix = "-" + dct['long_name']
    
            # set geocode data                  
            row['County'] = county
            row['Postal Code'] = postal_code_base + postal_code_suffix
            row['Latitude'] = result[0]['geometry']['location']['lat']
            row['Longitude'] = result[0]['geometry']['location']['lng']
            
            # check if geocode is an exact match
            if 'partial_match' in result[0]:
                row['Partial Match'] = 1
            else:
                row['Partial Match'] = 0
        
        except:
            row['County'] = ''
            row['Postal Code'] = ''
            row['Latitude'] = ''
            row['Longitude'] = ''
            row['Partial Match'] = 'INVALID'

        # output to console for diagnostics
        print row
        
        # output to output file
        writer.writerow(row)            

        # re-initialize variables for next address
        postal_code_base = ''
        postal_code_suffix = ''
        county = ''
                
        # pause between API requests per Google Maps API limitation
        #time.sleep(1)
        
    # close connections to both input and output files    
    infile.close()
    outfile.close()
