'''Code to take hop_list IP destinations and plot them on a world map, 
following the route from source to destination'''

# Notes: hop_list[0] is the destination IP address/geolocation
# the source IP address/geolocation hasn't been input into the code
# most likely the source IP address/geolocation is hop_list[1]

from trace_route import trace_route(hop_list)
import folium
import geocoder

def draw_map():

    # make a basemap, starting point
    map = folium.Map(
        location=[34.05, 118.24], #lat/long Los Angeles, CA
        zoom_start=5, # zoom level
        tiles= "CartoDB dark matter",
        #tiles= "Mapbox Control Room",
    )

    # add markers for each hop to the map
    for hop in trace_route: # how do you call hops in the hop_list from traceroute? Do I need to create a database or can I work off the list?
        hop = trace_route[0]

        # define text at each marker
        text = "IP Addr " + str(hop["ip address"]) + "Location " + str(hop["geolocation"])

        # plot map
        folium.CircleMarker(
            location= [hop["location"]], # location is defined by coordinates at latitude & longitude
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
