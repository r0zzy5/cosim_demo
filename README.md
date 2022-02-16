# cosim_demo
## Install docker:
### How:
- if using windows or mac you should install docker desktop which will include docker-compose
- if on raspberry pi or linux, you need to also install docker-compose after installing docker (instructions - ???)
	
### Testing:
To test docker works, in the terminal enter "docker run hello-world". You should then see the container created in docker desktop if using windows or mac or a hello world message in the linux terminal if using linux.
	
### Troubleshooting:
- docker error saying virtualisation not enabled (Windows):
    1. check whether it is disabled (instructions ???)
    2. enable this in the bios (instructions differ depending on machine. I did this by pressing f10 on boot but you would need to google how to do so for your machine)


## Install rancher:
### First time installation:
1. create a file called docker-compose.yml
2. copy the below text into this file (ensuring you don't use tab spaces):
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
3. in a terminal cd to the folder where you have saved this file and run the cmd `docker-compose up -d`
4. open "https://localhost" in a browser. This may take a few minutes but should show the rancher login page. This may also take you to a page saying the site is unsafe - if you select advanced settings you should be able to proceed to the site regardless.
5. once on the rancher login page, go back to the terminal and enter the cmd `docker-compose logs | grep "Bootstrap Password"`
6. this cmd should have given you a password to use to login to rancher. Rancher will then ask you to create a new password, after which you should be in the dashboard.
		
### Using rancher post first installation:
1. repeat steps 3 and 4 in 'First time installation'.
2. the username will be "admin" and the password will be the one you created in step 6 of 'First time installation'.
	
### Troubleshooting:
- the grep cmd might not be recognised by some terminals (Powershell). You may need to use a linux terminal.
	
## Setting the demo up:
### Setting up the server and viewer:
1. ensure you have a version of python > python3.10 as your default python version.
2. open a new terminal in visual studio code.
3. in this terminal enter the cmd `python -m venv venvname` where venvname is the name of the virtual environment you are ceating and can be whatever name you wish. You may need to install a python package to create virtual environments - the terminal should prompt you if this is needed.
4. close that terminal and open a new one again in visual studio code. This new terminal should now show that it is in the virtual environment you created.
5. in this terminal enter the cmd `pip install -r requirements.txt`. This should install the packages in that .txt file.
6. in a different terminal enter the cmd `python server.py`. This should start the websocket on port 8001.
7. in another terminal enter the cmd `python -m http.server`. You should now be able to see the viewer if you go to "localhost:8000" in any browser.
	
### Setting up a client locally:
1. set up the server and viewer
2. in another terminal in visual studio code enter the cmd `python client.py`. This will start a client and you should now see a red dot in the viewer on the browser.
3. repeat step 2 in a different terminal to add more dots.
		
### Setting up a client using docker-compose:
1. set up the server and viewer.
