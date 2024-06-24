'''Code to take hop_list IP destinations and plot them on a world map, 
following the route from source to destination'''

# Notes: hop_list[0] is the "header" line
# hop_list[1] is the destination IP address/geolocation
# the source IP address/geolocation hasn't been input into the code
# most likely the source IP address/geolocation is hop_list[2]

import trace_route
import folium
import geocoder
from geopy.geocoders import Nominatim

def draw_map():

    # hardcoding destination
    destination = "www.airbnb.com"

    # import hop_list
    hop_list = trace_route.trace_route(destination)
    print(hop_list)

    # make a basemap, starting point
    map = folium.Map(
        location=[34.05, 118.24], #lat/long Los Angeles, CA
        zoom_start=5, # zoom level
        tiles= "CartoDB dark matter",
        #tiles= "Mapbox Control Room",
    )

    # DbIPcity is not pulling lat/long, so here is code for city/state/country conversion
    # code to convert city, state, country to latitude/longitude
    def get_lat_long(city, state, country):
        geolocator = Nominatim(user_agent="geoapiExercises")
        location = geolocator.geocode(f"{city}, {state}, {country}")
        return location.latitude, location.longitude


    # add markers for each hop to the map
    for hop in hop_list: # how do you call hops in the hop_list from traceroute? Do I need to create a database or can I work off the list?
        hop = hop_list[1]

        # define text at each marker
        text = "IP Addr " + str(hop["ip address"]) + "Location " + str(hop["geolocation"])

        # setting up an if loop to identify hops with IP/Geo info
        if hop["ip address"] != "* * *" and hop["geolocation"] != None:

            # get the city, state, country from the hop
            #hop_geo = hop["geolocation"]
            hop_city, hop_state, hop_country = hop["geolocation"]

            # getting latitude and longitude from hop_geo
            lat, long = get_lat_long(hop_city, hop_state, hop_country)

            # plot map
            folium.CircleMarker(
                location= [lat, long],
                radius= 5, # circle size
                popup= text, # popup text window for each hop
                color= "#00FFFF", # cyan/aqua
                width= 1,
                fill= True, # fill marker with fill_color
                fill_color = "#00FFFF", # fill color set same as outline color - OPT. differentiate colors based on open/close countries
                fill_opacity= 0.9, #90% opacity = 10% transparency
            ).add_to(map)

    #map.save("traceroutemap.html") # save as html file, for future display
    map

if __name__ == "__main__":
    print(draw_map())
