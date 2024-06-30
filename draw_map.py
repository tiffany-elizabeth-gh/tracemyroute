'''Code to take hop_list IP destinations and plot them on a world map, 
following the route from source to destination'''

# Notes: hop_list[0] is the "header" line
# hop_list[1] is the destination IP address/geolocation
# the source IP address/geolocation hasn't been input into the code
# most likely the source IP address/geolocation is hop_list[2]

import trace_route
import folium
import webbrowser

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
        #tiles= "CartoDB dark matter",
        tiles= "cartodb positron",
    )


    # add markers for each hop to the map
    for hop in hop_list:

        # define text at each marker
        text = (f"'IP Addr:' + {str(hop["ip"])}\n"
                f"'Location:' + {str(hop["city"])} + {str(hop["region"])} + {str(hop["country"])}\n"
                f"'Lat/Long:' + {str(hop["latitude"])} + {str(hop["longitude"])}")

        # setting up an if loop to identify hops with IP/Geo info
        if hop["ip"] != "* * *" and hop["latitude"] != "N/A":

            # plot map
            folium.CircleMarker(
                location= [hop["latitude"], hop["longitude"]],
                radius= 5, # circle size
                popup= text, # popup text window for each hop
                color= "#00FFFF", # cyan/aqua
                width= 1,
                fill= True, # fill marker with fill_color
                fill_color = "#00FFFF", # fill color set same as outline color - OPT. differentiate colors based on open/close countries
                fill_opacity= 0.9, #90% opacity = 10% transparency
                ).add_to(map)
            print(hop)

    # to view map
    map.save("traceroutemap_test.html") # save as html file, for future display
    webbrowser.open("traceroutemap_test.html") # open html file in browser

    return map

if __name__ == "__main__":
    print(draw_map())
