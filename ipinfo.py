# MY IP SCANNER PROJECT
# need to fix some things


import os
import requests
import json
import time
import pyfiglet
import socket
from colorama import init, Fore

init()
GREEN = Fore.GREEN
RESET = Fore.RESET
GRAY = Fore.LIGHTBLACK_EX
Bl = '\033[30m'
Re = '\033[1;31m'
Gr = '\033[1;32m'
Ye = '\033[1;33m'
Blu = '\033[1;34m'
Mage = '\033[1;35m'
Cy = '\033[1;36m'
Wh = '\033[1;37m'



banner = pyfiglet.figlet_format("IP SCANNER")



def ip_whois(ip):
	print(f"{Gr}======IP INFO======")

	req_api =  requests.get(f"http://ipwho.is/{ip}")
	ip_data = json.loads(req_api.text)
	print(f"{Wh}\n IP target       :{Gr}", ip)
	print(f"{Wh} Type IP         :{Gr}", ip_data["type"])
	print(f"{Wh} Country         :{Gr}", ip_data["country"])
	print(f"{Wh} Country Code    :{Gr}", ip_data["country_code"])
	print(f"{Wh} City            :{Gr}", ip_data["city"])
	print(f"{Wh} Continent       :{Gr}", ip_data["continent"])
	print(f"{Wh} Continent Code  :{Gr}", ip_data["continent_code"])
	print(f"{Wh} Region          :{Gr}", ip_data["region"])
	print(f"{Wh} Region Code     :{Gr}", ip_data["region_code"])
	print(f"{Wh} Latitude        :{Gr}", ip_data["latitude"])
	print(f"{Wh} Longitude       :{Gr}", ip_data["longitude"])
	lat = int(ip_data['latitude'])
	lon = int(ip_data['longitude'])
	print(f"{Wh} Maps            :{Gr}", f"https://www.google.com/maps/@{lat},{lon},8z")
	print(f"{Wh} EU              :{Gr}", ip_data["is_eu"])
	print(f"{Wh} Postal          :{Gr}", ip_data["postal"])
	print(f"{Wh} Calling Code    :{Gr}", ip_data["calling_code"])
	print(f"{Wh} Capital         :{Gr}", ip_data["capital"])
	print(f"{Wh} Borders         :{Gr}", ip_data["borders"])
	print(f"{Wh} Country Flag    :{Gr}", ip_data["flag"]["emoji"])
	print(f"{Wh} ASN             :{Gr}", ip_data["connection"]["asn"])
	print(f"{Wh} ORG             :{Gr}", ip_data["connection"]["org"])
	print(f"{Wh} ISP             :{Gr}", ip_data["connection"]["isp"])
	print(f"{Wh} Domain          :{Gr}", ip_data["connection"]["domain"])
	print(f"{Wh} ID              :{Gr}", ip_data["timezone"]["id"])
	print(f"{Wh} ABBR            :{Gr}", ip_data["timezone"]["abbr"])
	print(f"{Wh} DST             :{Gr}", ip_data["timezone"]["is_dst"])
	print(f"{Wh} Offset          :{Gr}", ip_data["timezone"]["offset"])
	print(f"{Wh} UTC             :{Gr}", ip_data["timezone"]["utc"])
	print(f"{Wh} Current Time    :{Gr}", ip_data["timezone"]["current_time"])
	
	
	
def is_port_open(host, port):
	s = socket.socket()
	try:
		s.connect((host, port))
		s.settimeout(0.2)
	except:
		return False
	else:
		return True



def main():
	print(banner)
	try:
		print(f"{Gr}OPTIONS:")
		print(f"{Gr}[1] {Cy}Scan IP   {RESET}")
		print(f"{Gr}[2] {Cy}Port Scan   {RESET}")
		option = input("\nWhat would you like to do? ")
		option = int(option)
		if option == 1:	
			ip = input("What IP do you want to scan? ")
			ip_whois(ip)
		elif option == 2:
			host = input("Enter the host: ")
			for port in range(1, 1025):
					if is_port_open(host, port):
						print(f"{GREEN}[+] {host}:{port} is open    {RESET}")
	except KeyboardInterrupt:
		print("\nProgram interrupted by user. Exiting...")
		exit(0)

		
main()
