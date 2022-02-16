# cosim_demo
## Install docker:
### How:
- If using windows or mac you should install docker desktop which will include docker-compose.
- If on raspberry pi or linux, you need to also install docker-compose after installing docker (instructions - ???).
	
### Testing:
To test docker works, in the terminal enter "docker run hello-world". You should then see the container created in docker desktop if using windows or mac or a hello world message in the linux terminal if using linux.
	
### Troubleshooting:
- Docker error saying virtualisation not enabled (Windows):
    1. Check whether it is disabled (instructions ???).
    2. Enable this in the bios (instructions differ depending on machine. I did this by pressing f10 on boot but you would need to google how to do so for your machine).


## Install rancher:
### First time installation:
1. Create a file called docker-compose.yml.
2. Copy the below text into this file (ensuring you don't use tab spaces):
```
version: '3.3'
services:
	rancher:
		restart: unless-stopped
		ports:
			- '80:80'
			- '443:443'
		privileged: true
		image: 'rancher/rancher:latest'
```
3. In a terminal cd to the folder where you have saved this file and run the cmd `docker-compose up -d`.
4. Open "https://localhost" in a browser. This may take a few minutes but should show the rancher login page. This may also take you to a page saying the site is unsafe - if you select advanced settings you should be able to proceed to the site regardless.
5. Once on the rancher login page, go back to the terminal and enter the cmd `docker-compose logs | grep "Bootstrap Password"`.
6. This cmd should have given you a password to use to login to rancher. Rancher will then ask you to create a new password, after which you should be in the dashboard.
		
### Using rancher post first installation:
1. Repeat steps 3 and 4 in 'First time installation'.
2. The username will be "admin" and the password will be the one you created in step 6 of 'First time installation'.
	
### Troubleshooting:
- The grep cmd might not be recognised by some terminals (Powershell). You may need to use a linux terminal.
	
## Setting the demo up:
### Setting up the server and viewer:
1. Ensure you have a version of python > python3.10 as your default python version.
2. Open a new terminal in visual studio code.
3. In this terminal enter the cmd `python -m venv venvname` where venvname is the name of the virtual environment you are ceating and can be whatever name you wish. You may need to install a python package to create virtual environments - the terminal should prompt you if this is needed.
4. Close that terminal and open a new one again in visual studio code. This new terminal should now show that it is in the virtual environment you created.
5. In this terminal enter the cmd `pip install -r requirements.txt`. This should install the packages in that .txt file.
6. In a different terminal enter the cmd `python server.py`. This should start the websocket on port 8001 (assuming that the server "port" argument hasn't been changed from the default).
7. In another terminal enter the cmd `python -m http.server`. You should now be able to see the viewer if you go to "localhost:8000" in any browser.
	
### Setting up a client locally:
1. Set up the server and viewer.
2. In another terminal in visual studio code enter the cmd `python client.py`. This will start a client and you should now see a red dot in the viewer on the browser.
3. Repeat step 2 in a different terminal to add more dots.
		
### Setting up a client using docker-compose:
1. Set up the server and viewer.
2. Confirm the ip address of the network you would like to use. You can do this by entering the cmd `ifconfig` if using linux/mac or use the cmd `ipconfig` if using Powershell.
3. Open the client-compose.yml file. Within this change the WEBSOCKET_SERVER variable so that it reads your ip address followed by `:8001` (assuming that the server "port" argument hasn't been changed from the default). For example `WEBSOCKET_SERVER: '172.20.10.5:8001'`.
4. In a new terminal in visual studio code enter the cmd `docker-compose -f client-compose.yml up`.

### Setting up the client using rancher:
1. Set up the server and viewer.
2. Login to rancher using above instructions.
3. Create a new deployment in rancher.
4. Add the image "rnbrocks/cosim_demo:latest".
5. Confirm the ip address of the network you would like to use. You can do this by entering the cmd `ifconfig` if using linux/mac or use the cmd `ipconfig` if using Powershell.
6. Add the environment variable pair of `WEBSOCKET_SERVER` and `your_ip_address:8001` (similar to step 3 of "Setting up a client using docker-compose"). Replace "your_ip_address" with the ip address of your network.
7. Set the replica value to 1.
8. Save the deployment and the dot should appear in the viewer screen. This might take a bit of time but you should see the status "containercreating" in rancher.
