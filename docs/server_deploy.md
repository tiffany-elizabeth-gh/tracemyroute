# Server Deploy Guide
This guide covers deploying the tracemyroute application on a server environment, specifically PythonAnywhere. While there are PythonAnywhere-specifics to deploy, this guide will hopefully be helpful to future deployments in other server environments.

## Overview
If you haven't already, it would be helpful to review the tracemyroute [Developer's Guide](https://github.com/tpugh-ia/tracemyroute/blob/main/docs/developer_doc.md#developers-guide) for a more thorough overview. This guide will just go over the steps to deploy in a PythonAnywhere environment.

### PythonAnywhere
>PythonAnywhere is an online integrated development environment and web hosting service based on the Python programming language. Founded by Giles Thomas and Robert Smithson in 2012, it provides in-browser access to server-based Python and Bash command-line interfaces, along with a code editor with syntax highlighting.
>
>Source: [Wikipedia](https://en.wikipedia.org/wiki/PythonAnywhere)

PythonAnywhere is a great place to get started when working with python code and wanting to bring your code creations to the world wide web. It is easy to get started and free plans are available.
If you don't have an account already, it is easy to get started! [Register here](https://www.pythonanywhere.com/registration/register/beginner/) or if you want to learn more visit [PythonAnywhere](www.pythonanywhere.com)

### IPInfo
Just as with the internal deployment of this application, an API key from IPInfo is needed for server deployment. If you haven't done so already, obtain a free API key from [IPInfo](https://ipinfo.io/). For further instructions, read the [Developer's Guide](https://github.com/tpugh-ia/tracemyroute/blob/main/docs/developer_doc.md#developers-guide).

## Steps to Deploy
1. Create/Login in to your PythonAnywhere Account
2. Navigate to the Console tab and open a Bash Console
3. You should find yourself in your "mysite" folder.
4. Git Clone the tracemyroute server_deploy repository.
##
    git clone -b server_deploy --single-branch https://github.com/tpugh-ia/tracemyroute.git

5. Now you should have a new directory in your <mysite> directory titled "tracemyroute". You can check this by typing "ls" into the bash console terminal and it should show a list of directories in <mysite> including "tracemyroute".
6. (This step can also be done directly in the Bash console, whatever you prefer.) Whether in the same window or a new window, navigate to the Files tab. (IMPORTANT: Do NOT close/exit the Bash console. It needs to remain active for the virtual environment of your application.)
7. In the Files tab, navigate to <mysite>/tracemyroute and locate the api_keys.py.template file. Edit this file, replacing <your key here> with your "API Key" (don't forget to include " " around your API key string).
8. In your Bash console, change directories to tracemyroute/ and rename the api_keys file to be just api_keys.py
##
    mv api_keys.py.template api_keys.py

9. Navigate to the Web tab within your PythonAnywhere profile to set up your environment.
10. Scroll down to where you'll see Code: and Virualenv:
![584_pythonanywhere_setup](https://github.com/user-attachments/assets/cb7f0503-9b31-4e22-97b6-a0fd2c56cc44)


    You'll want to make sure to set up your Source code and Working directory to point to the correct directories. Your's should say "/home/<mysite>/tracemyroute/" and "/home/<mysite>/" where <mysite> is replaced by your site name.

11. The WSGI configuration file should automatically be populated, click it to make sure that the environment is set up properly. Once you click the link, it should look something like this:
![pythonanywhere_wsgi](https://github.com/user-attachments/assets/76a716bf-1f88-461c-8d5d-2e90812a313a)

12. If you've made any changes to your wsgi.py file be sure to Save.
13. Navigate back to the Web tab, scroll down to the Code: section and check that the Python version is 3.10 (or higher, but PythonAnywhere as of 2024 hasn't released any version of Python higher than 3.10).
14. Scroll back up to the top of the Web tab and click "Reload <mysite>/pythonanywhere.com". Wait for the spinning wheel to stop and click the link located under Configuration for <mysite>.pythonanywhere.com
16. Your server is live and ready!

## Code Notes
There were a couple of adjustments to the code that had to be done in main.py for it to work on a server like PythonAnywhere that we thought would be important to draw your attention to.

- Import sys, this was added in order for the virtual environment to locate the correct directories and files necessary to deploy the application.
- Because of the directories within PythonAnywhere, the pythonanywhere environment needed to be set up before the application code is ran, this involved adding an if loop identifying the PYTHONANYWHERE_SITE as the operating system environment. If the pythonanywhere environment is active, there is a command to change directory to "tracemyroute". We've added a print call for debugging within the pythonanywhere server log.
- The main difference between the internal environment and the pythonanywhere server is the ability to call the geojson url. Pythonanywhere didn't work well with this so the geojson file is added and configured for global access, simiarly to the Cyber_security.csv.
- In **display_hop_data()** the return is changed to include a response header ['X-Accel-Buffering'] which is needed for nginx, specific to PythonAnywhere
- Changing the geojson file to a global variable, meant changing the code for folium.Chloropleth from collecting geo_data from a URL to the global variable: geojson_data

## Potential Issues
The deployment came about through a lot of trial and error and community troubleshooting. Some hurdles to navigate that became critical for it to work was calling the PythonAnywhere environment correctly and identifying the environment appropriately. Errors with this still could occur and could require further troubleshooting. Due to the nature of PythonAnywhere and free accounts, servers can often overload quickly, which could cause temporary errors in the running of this application. As this is newly deployed, we are also aware that there may be more issues to overcome in the smooth running of this application on an external server. That is why this code lives in a dedicated server_deploy branch (and not part of the official tracemyroute v1.0.0 release) for further debugging and finessing.



