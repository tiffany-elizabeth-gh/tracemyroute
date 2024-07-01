'''Code to build flask app for user access and display of 
hop maps tracing an ip/web search'''


import subprocess
import socket
import ipinfo
import folium
import webbrowser
from folium.plugins import MarkerCluster
import requests
import flask
from flask import Flask, redirect, url_for, request, render_template, jsonify, send_file
from markupsafe import Markup

app = Flask(__name__)
access_token = input("enter ipinfo.io access token: ")
handler = ipinfo.getHandler(access_token)

@app.route("/")
def start_trace():
    return flask.render_template('basic.html')

@app.route("/tracemyroute", methods=["POST"])
def display_map():
    '''This function takes the user input and returns the map'''
    if request.method == "POST":
        destination = request.form.get("destination")
        if not destination:
            return "Please enter a destination.", 400
        else:
            # define max_hops
            max_hops = 30

            # get destination ip
            destination_ip = socket.gethostbyname(destination)

            # print traceroute command
            print(f"running traceroute on {destination} at {destination_ip}")

            # setting initial hop count
            hop_count = 0
            
            # create hop list for IP addresses
            hop_list = []

            # define traceroute
            traceroute = subprocess.Popen(["traceroute", "-w", "10", destination], 
                                        stdout=subprocess.PIPE, 
                                        stderr=subprocess.STDOUT,
                                        text=True)
            first_line = True

            
            while True:
                # get output from traceroute
                output = traceroute.stdout.readline()
                if not output:
                    break # no more output
                
                # skip anything starting with traceroute as not hop
                if output.startswith("traceroute"):
                    continue

                hop = output.split()
                hop_count = hop_count + 1

                # error handling for unresponsive hops
                if output.endswith("*\n"):
                    hop_list.append({"ip": "* * *", "hostname": "N/A", "country": "N/A", 
                                    "city": "N/A", "region": "N/A", "latitude": "N/A", "longitude": "N/A"})
                    max_hops -= 1
                    if max_hops == 0:
                        print("Max hops reached")
                        break
                else: 
                    # reviewing hop details
                    for tok in output.split():
                        if tok.endswith(")"): # find token ending in )
                            ip = tok[1:-1] # remove ()s
                            break
                    else:
                        continue 

                    hop_details = handler.getDetails(ip)

                    hop_dict = {}
                    for key in ["ip", "hostname", "country", "city", "region", "latitude", "longitude"]:
                        if key in hop_details.all:
                            hop_dict[key] = hop_details.all[key]
                        else:
                            hop_dict[key] = "N/A"
                    print(hop_dict)

                    hop_list.append(hop_dict)
            
            
            # make a basemap, starting point
            map = folium.Map(
                location=[34.05, 118.24], #lat/long Los Angeles, CA
                zoom_start=5, # zoom level
                tiles= "cartodb positron",
            )

            marker_cluster = MarkerCluster().add_to(map)

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
                        ).add_to(marker_cluster)
                    print(hop)

        
            # save map
            map.save("templates/traceroutemap_test.html")

    #return render(request, "traceroutemap_test.html")
    return "Traceroute complete."

@app.route("/map")
def display_map_html():
    return render_template("traceroutemap_test.html")

if __name__ == "__main__":
    app.run()




#@app.route("/")
#def flask_app():
    #return flask.render_template('traceroutemap_test.html')