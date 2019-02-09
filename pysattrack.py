#!/usr/bin/python3

"""
Python Satellite Tracker
Written by Cody Skinner, WX4WCS
Version: 0.0.1
This release requires an API key, see the README for details

TODO: add function to get lat/long from gridsquare
"""
import argparse
import configparser
import sys
import json
import requests
import ast
import time
from datetime import datetime, timedelta

#Get data from config file
config = configparser.ConfigParser()
config.read('settings.conf')
apikey = config['DATA']['APIKey']
olat = config['DATA']['Latitude']
olong = config['DATA']['Longitude']

#Get command line arguments
parser = argparse.ArgumentParser(description="Calculate upcoming satellite passes")
parser.add_argument("satid", help="NORAD Satellite ID")
parser.add_argument("days", help="Days to predict (max: 10)")
args = parser.parse_args()

#Make sure days is under the max
if (int(args.days) > 10):
    print("Days must be no greater than 10")
    sys.exit(0)

satid = args.satid
alt = "0"
days = args.days
minvis = "30"
url = 'https://www.n2yo.com/rest/v1/satellite/radiopasses/'+satid+'/'+olat+'/'+olong+'/'+alt+'/'+days+'/'+minvis+'/&apiKey='+apikey
response = requests.get(url)
data = response.json()

# Output
satname = data["info"]["satname"]
print("Satellite: " + satname)
passescount = data["info"]["passescount"]
print(str(passescount) + " upcomming passes")

#Loop through passes
count = 0
for i in data["passes"]:
    print('\n')
    passcount = count + 1
    print("PASS: "+ str(passcount))
    startUTC = data["passes"][count]["startUTC"]
    starttime = datetime.fromtimestamp(startUTC)
    print("AOS Time (UTC): " + str(starttime))
    maxUTC = data["passes"][count]["maxUTC"]
    peaktime = datetime.fromtimestamp(maxUTC)
    print("Peak Time (UTC): " + str(peaktime))
    endUTC = data["passes"][count]["endUTC"]
    endtime = datetime.fromtimestamp(endUTC)
    print("EOS Time (UTC): " + str(endtime))
    maxel = data["passes"][count]["maxEl"]
    print("Max elevation: " + str(maxel))
    startaz = data["passes"][count]["startAz"]
    print("Start Azimuth: " + str(startaz))
    maxaz = data["passes"][count]["maxAz"]
    print("Peak Azimuth: " + str(maxaz))
    endaz = data["passes"][count]["endAz"]
    print("End Azimuth: " + str(endaz))
    count = count+1

