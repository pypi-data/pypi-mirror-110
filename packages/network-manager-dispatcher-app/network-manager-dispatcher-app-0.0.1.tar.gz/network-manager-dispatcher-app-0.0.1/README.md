# DNS Leak Test
## **A Job for NetworkManager dispatcher.d**

[![Build Status](https://travis-ci.com/meads/network-manager-dispatcher-app.svg?branch=main)](https://travis-ci.com/meads/network-manager-dispatcher-app) 

[![codecov](https://codecov.io/gh/meads/network-manager-dispatcher-app/branch/main/graph/badge.svg?sanitize=true)](https://codecov.io/gh/meads/network-manager-dispatcher-app)

Network Manager dispatcher scripts - allows you to respond to events on network interfaces by implementing a simple interface and staging the scripts according to a certain pattern.

## How is it used?

After installing and configuring for an ssid on your machine, it runs automatically in the background by NetworkManager executing the configured scripts for us when the network events are received.

When you boot up and your computer establishes a connection with the outside world you will begin to hear a telephone dialing sound during the query to the bash.ws site. Upon receipt of the dnsleaktest results, one of three sounds are played indicating the results:
    
    1. A bell is played. A bright "ding" is played when the dnsleaktest results are that "DNS is not leaking".
    
    2. A dissonant shrill sound is played indicating that "DNS is probably leaking".

    3. A telephone dial tone is played indicating "No internet connection."

Based on this sound you can carry on as usual with your online session or take the appropriate action with your VPN connection etc. to ensure that you aren't leaking DNS for whatever reason. This was largely for making my current setup easier to work with. My setup will not alow any connected devices to have outside access until the VPN tunnel has been established, but I was still having to test the DNS leaking manually each time. Now I can just wait for the bell!   

## Install 📩

```bash
# 1. clone the repo
git clone https://github.com/meads/network-manager-dispatcher-app

# 2. change directory to the repo
cd network-manager-dispatcher-app

# 3. (optional) update the bash.ws/dnsleak.sh script
make update-lib

# 4. install a configuration using the provided menu.
make

# A menu will be displayed like below allowing a numeric choice for
# the interface we want to have the leak tests performed on each time
# we connect. Press 1 here for "House" ssid.

SELECT   NAME              UUID                                  TYPE  DEVICE    
1)       House             a0c725bd-958e-4057-a941-184f1f556257  wifi  wifi0    
2)       Guest             8c7d89d5-8216-4989-b972-ae890abc5c85  wifi  --        
```

## Post Installation Verification ✔️
```bash
# NOTE: you may want to run `make logs` prior to this command to see the application logs as they are written."

# Should hear a dial tone after running this command
make wifi-off

# Should hear a telephone ringing after running this command, having previously run the above command.
make wifi-on
```

## Diagnose 🕵️

```bash
# This will open the logs file to view during or after the connection/disconnection process to see the details.
make logs
```

## Kill it with fire!!! 🔥

```bash
# If something has malfunctioned and the sounds are in a loop or whatever, just run the following to kill the process.
make kill-rogue-sound-threads
```

## Remove 🗑️

```bash
# This will remove any configurations currently under /etc/NetworkManager/dispatcher.d/ and will prompt for root password.
make clean
```

*Note: The intention is to allow for multiple configurations, hence the usage of the device UUID used throughout each configuration generated after running `make` and selecting a number from the menu. However usage of multiple configurations is experimental at the moment.*

## Deploy 🚀
*These steps are for me*
1. create separate commit with version bumps in Makefile "install" target where version is specified at the end of the command. Also update
   the setup.cfg version.
2. push the changes to github.
3. `make distribute` (creates a new distribution in the PyPi index)


## Thanks!

Thanks to github user macvk for contributing what is known here as bash.ws/dnsleak.sh script which can also be [found here](https://bash.ws/dnsleak).
