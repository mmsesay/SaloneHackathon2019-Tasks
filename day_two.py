from flask import Flask, request
from datetime import datetime, date
import logging
from typing import List, Tuple, Dict, Optional
import time
import re
import pymysql
import requests
import json
import pprint

import csv

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

username = "pdtpatrick"
password = "u3!WL2uC0dxu"
# in seconds
start_time = 3600 * 48  # 48 hours
# airport code
# airport = "KSEA" # Frankfurt
airport = "EDDF"  # Frankfurt

filename = './airports.csv'

def read_airport(filename: str) -> Dict[str, str]:
    keys = [
        "id",
        "name",
        "city",
        "country",
        "IATA",
        "ICAO",
        "latitude",
        "longitude",
        "altitude",
        "timezone",
        "dst",
        "tz",
        "type",
        "source",
    ]
    airports = csv.DictReader(
        open(filename), delimiter=",", quotechar='"', fieldnames=keys
    )
    d = {airport["ICAO"]: airport for airport in airports}
    return d

def call_api(airport: str = None) -> Dict[str, str]:
    """Call opensky API and return all departures
    begin = now - days ago
    end = now
    """
    current_time = time.time()
    URL = f"https://opensky-network.org/api/flights/departure?airport={airport}&begin={int(current_time) - start_time}&end={int(current_time)}"
    logging.info(f"URL is now: {URL}")
    r = requests.get(URL, auth=(username, password))
    if r.status_code == 404:
        logging.error("Cannot find data")
        return None
    assert len(r.json()) != 0
    return r.json()

def process_coordinates(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process Coordinates
    Pull data from opensky api, read the csv and create an output like:
    List[Dict[Dict[str, str]]]
    Meaning, we'll have a List[Airport[Coordinates[longitude, latitude]]]
    """
    fetchedData = call_api(airport='EGLL')
    # EDDF

    # passing the csv data to the variable
    csv_content = read_airport(filename)

    # passing the estDepartureAirport and estArrivalAirport
    estDept = fetchedData[0]['estDepartureAirport']
    estArrival = fetchedData[0]['estArrivalAirport']

    # they will hold the longitude and latitude
    depart_lat = ''
    depart_lon = ''
    arrival_lat = ''
    arrival_lon = ''

    # 
    try:
        # loop through the csv file
        for k,v in csv_content.items():

            # check for the depature
            if k == estDept:
                depart_lat = v['latitude']
                depart_lon = v['longitude']

            # check for the arrival
            if k == estArrival:
                arrival_lat = v['latitude']
                arrival_lon = v['longitude']

        # output
        output = [
            {estDept: 
                {
                    "longitude": depart_lat,
                    "latitude": depart_lon
                }
            },
            {estArrival: 
                {
                    "longitude": arrival_lat,
                    "latitude": arrival_lon
                }
            },
        ]
    except IndexError:
        print('--------------------------------------------------')
        logging.info(f'depature airport {estDept} or arrival {estArrival} is not found')
    
    
    return json.dumps(output)

def process_flights(start_time: int, end_time: int) -> List[Dict[str, str]]:
    """Process flight information
    Call the opensky api; this will return List[Dict[str, sr]]
    
    Remember our final output, we want to return:
    List[Dict[str, str]]
    In the Dict, we'll have departure, arrival. So something like:
    Dict[departure, arrival]
    The shouldn't be duplicates in your json returned. 
    """

    output = []
    fetchedData = call_api(airport)
    logging.info('The data is {fetchedData}')
    
    print('previous list length :' + str(len(fetchedData)))
    # estDept = fetchedData[0]['estDepartureAirport']
    # estArrival = fetchedData[0]['estArrivalAirport']

    f = {}
    data = []
    result = {}
    newList = []
    for dict_item in fetchedData:

        dp = [dict_item['estDepartureAirport']]
        ap = [dict_item['estArrivalAirport']]
        m = dict(zip(dp,ap))
        data.append(m)  # append the data

    
    # for i in range(0, len(data)):
    #     if data[i] not in data[i+1:]:
    #         newList.append(data[i])

        for i in range(len(data)): 
            if data[i] not in data[i + 1:]: 
                newList.append(data[i]) 
        
        # for k,v in m.items():
        #     if k not in et.keys():
        #         et[k] = k
        #         et[k] = v
        #         data.append(et)
        #     else: 
        #         et[k] = v
                # data.append(et)
    # data.append(et)
        # print(result)
    # print('len: ' + str(len(result)))
    
    # looping through the new dictionary 
    # for key,val in m.items():
    #     if key not in m.keys():
    #         m[key] = key  # adding the a new key
    #         m[key] = val  # adding the a value
    #     data.append(m)  # append the data
        

        # output.append(
        #     # dict_item['estArrivalAirport']
        #     f
        # )

        # output.append(
        #     {'departure_airport': estDept},
        #     # {'departure_airport': estArrival}
        # )

    # looping through the new dictionary 
    # for key,val in newDict.items():

    #     # check if the key not existing in the finalDict
    #     # Then add it 
    #     if key not in finalDict.keys():
    #         finalDict[key] = key  # adding the a new key
    #         finalDict[key] = val  # adding the a value
    #     else: 
    #         finalDict[key] += val  # summing up the values of new key to the existing key 


    # output variable
    # output = [
    #     {'departure_airport': estDept},
    #     {'departure_airport': estArrival}
    # ]

    print('final list length :' + str(len(newList)))
    # print(len(newList))
    return json.dumps(newList)

@app.route('/')
def index() -> str:
    """use this as a test to show your app works"""
    return f"Hello world!"


@app.route('/flights')
def flights() -> str:
    """API for flight information
    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: destination_airport},
        {departure_airport: destination_airport}
    ]
    Remember to add some logging so it is easy for you
    to troubleshoot. 
    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    # req = request.args()
    # call_api(airport)
    start_time = 1230
    end_time = 1300
    return process_flights(start_time, end_time)


@app.route('/coordinates')
def coordinates() -> str: 
    """API for coordinate information
    your API will receive `start_time` and `end_time`
    Your API will return a json in the form of
    [
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
        {departure_airport: 
            {
                "longitude": long,
                "latitude": lat
            }
        },
    ]
    Remember to add some logging so it is easy for you
    to troubleshoot. 
    Once you have your initial version, think about how you can
    scale your API. Also think about how you can speed it up
    """
    start_time = 1230
    end_time = 1500
    return process_coordinates(start_time, end_time)
