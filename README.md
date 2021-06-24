# pyftdcaps

## Problem Statement:
- Cisco Secure Firewall Threat Defense (FTD) does not allow an SCP "pull" where the FTD appliance acts as an SCP server
- Cisco ASA allowed itself to be an SCP server with the configuration command `ssh scopy enable`
- Often engineers work in the `system support diagnostic-cli` running L3/L4 captures from the LINA engine
- Once saved, unless one has an SCP to **push** the files *to* there is not an easy way to get the files off box for examination in tools like Wireshark
- This script uses the [pyftd](https://github.com/aaronhackney/pyftd) library and [netmiko](https://github.com/ktbyers/netmiko) to easily download a packet capture from an FDM managed FTD to your default home directory

## Requirements
- Python 3.7+
- pyftd 2.1.0+
- netmiko 3.4.0+
- FTD Version 6.6.0+ managed by FDM (Sorry, not FMC compatible)
- Admin credentials for the FTD

## Installation
Clone this repo
python -m pip install git+https://github.com/aaronhackney/pyftd.git
pip install netmiko

## Use
### Required Arguments
```
python captures.py [FTD management ip] [capture filename on disk0]  
```

### Optional switches
 -n ignore SSL/TLS warnings (self signed certificate)  
 -d debug log the netmiko SSH session to this directoy as `ssh_log.txt`  
 -p [password] provide the password at runtime. If omitted, you will be prompted for the admin password at runtime

## Example
### FTD Save Capture
```
fp66# copy /pcap capture:akh1 disk0:akh1.pcap
Source capture name [akh1]?
Destination filename [akh1.pcap]?
!!
120 packets copied in 0.0 secs
fp66#
```

### Download capture from FTD
```
python captures.py 172.30.4.28 akh1.pcap -p 'P@$$w0rd1!' -n

--- TLS warning messages omitted ---

File downloaded and saved at /Users/username/akh1.pcap
```


