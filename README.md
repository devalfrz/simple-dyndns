# simple-dyndns
This is a tool that allows you to use dynamic DNS servers for testing or personal
purposes by updating the DNS every time it is changed by your ISP. This tool requires
a "known location" and a simple script to keep the ip updated.

With this tool you can have your regular http://my-domain.com with your main site and
several subdomains each with a different domain name such as http://dev.my-domain.com or
http://home.my-domain.com.

## Features
- Hostmonster support
- Debian/Ubuntu server support

## Installation
Get and install [simple-dyndns-server](https://github.com/devalfrz/simple-dyndns-server) on a known server https://github.com/devalfrz/simple-dyndns-server.

Get dependencies:
```
sudo apt-get install python-dev libssl-dev
sudo pip install mechanize
```
Get the package:
```
git clone https://github.com/devalfrz/simple-dyndns
```
Add your own settings to the `simple-dyndns/config.py` file:
```python
SIMPLE_DYNDNS_SERVER = SimpleDynDnsServer(
    known_server='http://your-known-server.com/simple-dyndns-server/',#Replace with yor own server
    known_server_key='dyndns',#Replace with your own key
    server_alias='christine.behuns.com'#Replace with your own unique alias
)

DOMAINS = [
    Hostmonster(
        domain='your-domain.com',#Replace with your own domain
        username='hostmonster-username',#Replace with your own username
        password='hostmonster-password',#Replace with your own password
        records=['@','www','dev','mail',]#Replace with your own records
    ),
]
```
Test before permanently installing:
```bash
python simple-dyndns/loop.py
```
If you get no errors and the records are succesfully updated, then permanently
install in your system and create the daemon so it can run at startup:
```bash
sudo cp -a simple-dyndns /etc/simple-dyndns
sudo ln -s /etc/simple-dyndns/simpledyndns /etc/init.d/simpledyndns
sudo update-rc.d simpledyndns defaults
```
As any standard service on Debian and its cosins, manage the service by writing:
```bash
sudo service simpledyndns start # stop|restart
```
## Uninstall
To uninstall simply remove the daemon record from your server:
```
sudo service simpledyndns stop
sudo update-rc.d -f simpledyndns remove
```

## To-Do
This program currently supports Hostmonster but it is written so it can eventually
support any other DNS such as Godaddy.com, Hostgator.com or Domain.com
If you have any suggestions please say hi on Twitter @alfrz
