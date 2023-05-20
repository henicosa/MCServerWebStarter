# MCServerWebStarter

This little flask web server allows users to start a minecraft server hosted on a different computer in the network.

## Install
First make changes according to your setup to the `secrets copy.json` file in the secrets folder and rename it to `secrets.json`.  
Then run `install.sh` in the main project directory. It will run the flask script inside a docker container and serves the web page on port 2112.
