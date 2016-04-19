gmaps
=====

Google Maps API scripts for getting map data. See Google's [documentation](https://developers.google.com/maps/documentation/javascript/tutorial) for more information.

### Public Transit Stats for Multiple Routes
##### Filename: [google_json-parse3.py](https://github.com/dnaeye/gmaps/blob/master/google_json-parse3.py)
Get public transit stats for multiple routes. Stats include total distance and duration as well as breakdowns by walking and transit, including the total number of stops. Inputted information for the origin and destination can be formatted in standard U.S. address syntax: street address, city, state, and zip code (e.g., 1234 Anyplace St., Anywhere, AW, 12345).

### GeocodeAddress
##### Filename: [geocode.py](https://github.com/dnaeye/gmaps/blob/master/geocodeaddress.py)
Get geocode data (postal code, GPS coordinates) for an address via the Google Maps API. Script also cleans the street address by removing any characters before the street number.

### Geocoder
##### Filename: [geocode_costco3.py](https://github.com/dnaeye/gmaps/blob/master/geocode_costco3.py)
Adapted from the original code in the book ["Visualize This"](http://book.flowingdata.com/), by Nathan Yau, for the Google Maps API v.3 and to write the received geodata to a .CSV file. Outputted data include the Costco warehouse number, address, and GPS coordinates (latitude, longitude).
