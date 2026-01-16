# OffLineMathLab2

HOST
Enable WSL on windows
Install Python (and PIP) - must be installed and added to the PATH
Install Docker
Start Docker
- TERMINAL
  docker build -t mathlab-inventory .  #include .
  
- TERMINAL
  touch database.json  # Creates an empty file first if one doesn't exist
  docker run -d \
  --name mathlab-server \
  --restart unless-stopped \
  --network host \
  -v "$(pwd)/database.json":/app/database.json \
  mathlab-inventory

_____________________________________________________________________________________________
*** if touch is not recognized replace with "type nul > database.json" and RUN the following
  docker run -d ^
  --name mathlab-server ^
  --restart unless-stopped ^
  --network host ^
  -v "%cd%/database.json":/app/database.json ^
  mathlab-inventory
_____________________________________________________________________________________________
*** if fails again use fail-safe 
  docker run -d ^
  --name mathlab-server ^
  --restart unless-stopped ^
  -p 8000:8000 ^
  -v "%cd%/database.json":/app/database.json ^
  mathlab-inventory
_____________________________________________________________________________________________

**MAYBE JUST TRY THIS INSTEAD OF ANY OF THE CODE ABOVE WHEN STARTING DOCKER from in Directory!!!

docker build -t mathlab-inventory .  #include .
docker run -d ^
**docker run -d --name mathlab-server --restart unless-stopped -p 8000:8000 -v "${PWD}/database.json:/app/database.json" mathlab-inventory****

HOST and SECONDARY
Install Tailscale to access 8000 port from the host computer on secondary computers
