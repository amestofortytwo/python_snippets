from datetime import datetime, timedelta
import json
import requests
import os
import concurrent.futures

lookback = 7

import os

filename = 'ips.txt'
# Create file if not existing
if not os.path.exists(filename):
    open(filename, 'w').close()

# Replace with your AlienVault API key
API_KEY = ""

# List of IP addresses to check
ips = []


# OTX_API_ENDPOINT = "https://otx.alienvault.com/api/v1/indicators/IPv6/{ip}/{malware}"
HEADERS = {"X-OTX-API-KEY": API_KEY}

def check_date(date_str):
    date = datetime.strptime(date_str.split('T')[0], '%Y-%m-%d')
    delta = datetime.now() - date
    if delta < timedelta(days=lookback):
        return True

triage_ips = []
with open('ips.txt', 'r') as f:
    existing_ips = set(f.read().splitlines())

with open('ips.txt', 'a') as f:
    with requests.Session() as session:
        def process_ip(ip):
            if ip in existing_ips:
                print(f"Skipping {ip} as it already exists in the file")
                return

            try:
                with session.get(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/reputation", stream=True) as reputation:
                    reputation.raise_for_status()
                    reputation_data = reputation.json()
                with session.get(f"https://otx.alienvault.com/api/v1/indicators/IPv4/{ip}/malware", stream=True) as malware:
                    malware.raise_for_status()
                    malware_data = malware.json()
                    date_values = [d['date'] for d in malware_data['data']]
                    for date in date_values:
                        if check_date(date):
                            triage_ips.append(ip)
                            print(ip)
                            f.write(f"{ip}\n")
                            break
            except requests.exceptions.HTTPError as e:
                print(f"Error: {e} for {ip}")
            except json.decoder.JSONDecodeError:
                print(f"Error: JSON decoding failed for {ip}")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.map(process_ip, ips)

print("Triage these IPs:", triage_ips)

#TODO add triage leveled files based on different time lookbacks. Avoid duplicates (like an ip in 7 days should not go into 30 days as well).
#TODO: Add "known goods" (Ips outside lookback) to its own file. Would make the program run faster if the IP's list is being updated.
#TODO: remove IPs if they dont exists in their respective (lookback) file any longer when the query with any exisitng ips is run for 2nd++ time.
