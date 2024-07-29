# Developer's Guide
This guide covers envivornment set up, user interaction flow, known issues, and future possibilites of tracemyroute.

## Overview
Tracemyroute is an interactive search engine allowing a user to search a destination and follow the path to get there (via hops), collecting information on each hop along the way. The hop data is displayed in a stream and then plotted on a folium map which is displayed in an html along with the full hop list and the option to start a trace again.
See [README](https://github.com/tpugh-ia/tracemyroute/blob/main/README.md#user-guide) for the general overview.

## Project Specs
This application currently includes the following functionality:
- Application that takes a user's input of a destination URL
- Upon initation, the destination URL is validated
- 	If the user enters an IP address, this is validated against proper IP address formatting using re.match
- 	A traditional URL is validated using socket.gethostbyname
- A valid destination is then traced with a stream of hop data displaying in the user's browser
- This hop data is logged and then used to develop a folium map
- 	The folium map is built with JSON and Chloropleth to draw countries and fill with color based on cybersecurity risk.
- 	The hops are designated with Markers displaying hop details and clustered using MarkerCluster to show where groups of hops are located, and lines are drawn between the hops to show the route from source to destiantion.
- 	Folium provides zoom capabilities and there are set zoom_starts based on distance between farthest hops.
- A successful traceroute presents the user with a results html page that displays the folium map, the hop list with details, and the opportunity to start a new trace.
- Unsuccessful traceroutes, due to an invalid destination input, unsuccessfully linking a destination URL to a hostname, or a traceroute resulting in no hops, result in a user being presented with an error html and given the opportunity to try again.

## Install Notes
General installation notes can be found in the [User Guide](https://github.com/tpugh-ia/tracemyroute/blob/main/README.md#user-guide).

1. Set up the environment (Python 3.10+ and requirements.txt)
2. Get API key and format api_keys.py file
3. Run main.py

For deploying this application on a web server like pythonanywhere, check out [server_deploy.md](https://github.com/tpugh-ia/tracemyroute/blob/7abc3751f4fbfbf2991fb5bd6cf283dc896eacc9/docs/server_deploy.md).

## User Interaction and Code Flow
The following is a walk through from start to finish of what happens as the user interacts with this application.

### main.py
As the name suggests, this is the core of the code and will call all necessary functions.
1. Upon launching, the application's Flask environment is set up and the API token is called. The **start_trace():** function begins, launching *begin_tracemyroute.html*.
   * *begin_tracemyroute.html* is a basic html set-up displaying a simple input form for the user to input a destination URL
   * After the user inputs a destination URL they have the option to click "Start Trace" with either a mouse or the Enter/Return key. This initiates the script function draw_map() which uses .ajax to call the main.py function /tracemyroute instructing that a success will result in the function(response) "/results"

![tracemyroute_begin](https://github.com/user-attachments/assets/a3013c3e-5791-4a73-96af-c24df6ca6c66)

2. "/tracemyroute" calls the application function **display_hop_data()** which uses the request library to pull the user's destination input and validates it through the function **dest_address()** imported from dest_address.py.
   * **dest_address()** identifies if the user input an IP address or URL, and verifies it.
   * If the verification is successful, the function returns True with the corresponding IP address.
   * If the verifcation is unsuccessful, the function returns False with a corresponding error message. If false is returned, **display_hop_data()** will return a redirect to *tracemyroute_error.html* The function **error(error_message)** is called to display *tracemyroute_error.html* inputting the corresponding error message.
   * *tracemyroute_error.html* is a basic html page displaying the linked error message and a button to initiate a new trace with a script that uses .ajax to call the function **start_trace():** and redirect the url to *begin_tracemyroute.html*

![tracemyroute_error](https://github.com/user-attachments/assets/8f0a3764-1c3a-46fc-8b91-6fc78af3b01b)

3. If the verification of the destination is successful and returns True the function **stream_hop_data(destination, source=False)** is initiated. This function is built to display the stream of hops to the user, appending each hop to the global variable hop_list[].
   * Within this function, the destination url is converted to an IP address and the source IP address is established through the function **source_address(source)** imported from the root file source_address.py.
   * **source_address() is coded with the potential of taking manual source IP address entry in the future, but currently handles source=False and uses the socket library to get the source IP address from the user's operating system. This source is returned to **stream_hop_data()** and a traceroute is performed.
   * Traceroute is accomplished through identifying the user's operating system and using the subprocess library to perform a traceroute. stdout and stderr are used to display the data found during the traceroute.
   * A while loop structures the traceroute output to identify the pertinent hop information necessary for building the folium map and hop details useful to the user.
   * Yield is used to display the hop data as it is discovered.
   * Upon completion, a button appears in the user's browser allowing them to "Plot Map." This button calls the **plot_map()** function.

![tracemyroute_stream](https://github.com/user-attachments/assets/31a18e91-099c-4f84-99b5-0297bea59219)
  
4. The **plot_map()** function builds, plots, and structures the folium map based on the hop_list returned from **stream_hop_data()**
   * **plot_map()** calls the function **get_lat_long_center(hop_list)** to structure the map to center and zoom based on the hop list and the distance between hops.
   * The base of the folium map is basic with added layers to create a more visually descriptive and interactive map for the user. <u>folium.Chloropleth</u> is used to add an overlay that pulls data from the "Cyber_security.csv" to color code security risks of the countries. A geojson feature is added to draw the country outlines.
   * <u>folium.CircleMarker</u> is used to plot the hop list and it is added to the <u>MarkerCluster</u> add on to visually display where hops overlap.
   * <u>folium.PolyLine</u> is used within a for loop to draw lines between the hops. Here the code differentiates between the hop_list and valid_hops to retrieve hops that have a longitude and latitude to work with and to loop through the valid_hops list.
   * The layered folium map is saved using a timestamp to the templates folder, and any previous map left in the templates folder is deleted - to save space and protect the privacy of prior searches.
   * Upon completion of building and plotting the folium map, a redirect is returned for the /results url calling the function **results(map)**

5. The **results(map)** function is the final display to the user. It uses the final hop_list and the completed folium map to build and return the *tracemyroute_results.html* page.
	* *tracemyroute_results.html* can be divided into three sections: Map, Results, and Begin Again.
 	* Map holds and displays the folium. It's style is defined within #map-container. The body display indicates the note to include map.
  	* Results holds and displays the hop data that is brought in from the **results()** function and looped through in the HTML to display the key:value to the user. The style of the Results is defined within #results-container.
  	* Begin Again is structured and functions similarly to both *begin_tracemyroute* with a simple input form and button to call the JavaScript function draw_map(). The style of Begin Again is defined in #begin-again.
  	* The script within *tracemyroute_results.html* involves an .ajaxSetup to clear the cache and a threefold function draw_map(). The threefold .ajax would not be necessary if the application was only to be used once, but because it is set up to receive reoccurring input, there was a need to clear the cached data and force html to pull new data to display.
  		* The first .ajax call restarts the traceroute with a new destination calling main.py's **/restart_trace** function to clear variables and return **stream_hop_data()**
   		* The second .ajax call forces html to retrieve a new map. With folium there were problems with reloading a map even when a new one replaced the old one, this worked to force a map reload. (Although this problem was treated from both the html side and the coding side with saving the maps with timestamps.
    	* The third .ajax call is to pull the new /results data from the **results** function that contains new hop data and a new map to display.

![tracemyroute_mapresults](https://github.com/user-attachments/assets/fdf3a279-88b8-4612-a45f-8fb6d4b7b709)
![tracemyroute_shanghai](https://github.com/user-attachments/assets/1316c4f5-7525-41a3-ad58-55d859db4c00)

6. The application is set up in a way to be continuous. The user can run as many traceroutes as they'd like and if they run into errors they can be brought again to the **start_trace()** function with the *begin_tracemyroute.html* page.

## Known Issues
Overall the code runs smoothly but there are areas still being worked through or puzzles not quite solved.
* The code runs well on a developer server but when it was attempted to set up the code in a web server platform like pythonanywhere or Render, the code failed to work. The two biggest hurdles involved the code requiring access to the user's operating system and this not being possible in a cloud-based server like Render, and it not being possible to be a superuser in pythonanywhere. This prevented future troubleshooting in a web-based environment. So more unknown errors could be possible.
 	* 	**Update:** Certain servery deploy strategies have been applied and work but there is still more debugging to be done. To get started in an environment like pythonanywhere, check out [server_deploy.md](https://github.com/tpugh-ia/tracemyroute/blob/main/docs/server_deploy.md#server-deploy-guide).
* It was the original intent to include a source IP address input but there was trouble with setting up accurate ways to verify the source IP address and integrating this within the traceroute function itself with subprocess. It appears that manually inputting a source IP address is only possible on certain operating systems (and does not include Windows).
* Considering the numerous ways a URL can be written, the current code only handles certain structures of URLs and does not include structures like apply.host.edu/page. So while apply.host.edu/page might be a valid URL it may return invalid URL if socket.gethostname cannot verify it. Although, there is current handling for this that works in some cases where URL is parsed through to fit within the UTF-8 structure.
* Timeout for a traceroute was not solved in this code rendition. Certain traceroutes can take a significant amount of time and currently there is not technical set-up for setting a maximum time to wait.

## Future Possibilities
While this code is a great base, there is a lot of potential on what could be done.
* One potential solution for making this application possible on a web server is manually writing the traceroute portion, building a traceroute function within this code (i.e. choosing TCP/UDP ports to connect to, creating ping packets, etc.) There are some great sources online that could be built into this but require more time and study.
* It would be great to distinguish the folium map lines more to visually display which hops came first and last, rather than simply connecting them.
* Adding in a timer to calculate the hop time distance would be a useful feature to add, not only for allowing the user to quit early, but also could add the potential for latency to be displayed within the folium map in the lines between hops.
* Visually there are a lot of touch-ups that can be done in the GUI, which would just take time and a willingness for trial and error.
	* The current visual doesn't display the original destination searched for, and I think this would be good to display on the /results page
	* Certain traceroutes can take a significant amount of time, and it would be cool to add an animation for the stream_hop_data page that is entertaining while the user is waiting.

## Ongoing Deployment/Development
While the project that initiated this application is closed, this is still a code that I see myself working on. I am new to python coding and this project has been a great place to practice and build upon the basics. It is also a place to stretch my creativity. I want to continue working through some of the following in my free time:
* Research deploying this code on a web server
* Adding a time element to the traceroute method
* Applying this time piece to the map
