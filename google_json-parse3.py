# import relevant python modules
import csv, json, requests, os, time

# import data file of student/school addresses
with open(os.path.expanduser("~/Documents/Code/Python/student_addresses.txt"), 'rU') as infile:
    reader = csv.DictReader(infile, delimiter='\t')
    
    # create output file for trip data via Google Maps API
    outfile = open(os.path.expanduser('~/Documents/Code/Python/student_addresses_out.txt'), 'wb')
    writer = csv.DictWriter(outfile, fieldnames=['student_number', 'lastfirst', 'origin', 'destination', 'total_distance', 'total_duration', 'walking_distance', 'walking_duration',
                                                 'transit_distance', 'transit_duration', 'transit_stops'], delimiter='\t')
    writer.writeheader()
    
    # create Google Maps API Directions request URL
    url = 'http://maps.googleapis.com/maps/api/directions/json?'
    
    # create request parameters from import file data
    for row in reader:
        row['origin'] = row['origin'].replace(' ','+')
        row['destination'] = row['destination'].replace(' ','+')
        params = dict(origin = row['origin'],
                      destination = row['destination'],
                      sensor = 'false',
                      departure_time = '1387238448',
                      mode = 'transit')
        data = requests.get(url=url, params=params)
        binary = data.json()
        
        # create new aggregate data based on requested data
        for route in binary['routes']:
            
            # initialize new dictionary keys for aggregate data
            row['total_distance'] = 0
            row['total_duration'] = 0
            row['walking_distance'] = 0
            row['walking_duration'] = 0
            row['transit_distance'] = 0
            row['transit_duration'] = 0
            row['transit_stops'] = 0
            
            # loop for each API request converts values into floats and aggregates them
            for leg in route['legs']:
                row['total_distance'] += float(leg['distance']['text'].replace("mi",""))
                row['total_duration'] += float(leg['duration']['text'].replace("mins",""))
                for step in leg['steps']:
#                    row['step'] = step['html_instructions']
                    if step['travel_mode'] == 'WALKING':
                        row['walking_distance'] += float(step['distance']['text'].replace("mi",""))
                        row['walking_duration'] += float(step['duration']['text'].replace("mins",""))
                    elif step['travel_mode'] == 'TRANSIT':
                        row['transit_stops'] += float(step['transit_details']['num_stops'])
                        row['transit_distance'] += float(step['distance']['text'].replace("mi",""))
                        row['transit_duration'] += float(step['duration']['text'].replace("mins",""))

        # format origin and destination data for output file
        row['origin'] = row['origin'].replace("+"," ")
        row['destination'] = row['destination'].replace("+"," ")
        
        # pause between API requests per Google Maps API limitation
        time.sleep(2)
        
        # output to console for diagnostics
        print row
        # output to output file
        writer.writerow(row)
    
    # close connections to both input and output files    
    infile.close()
    outfile.close()