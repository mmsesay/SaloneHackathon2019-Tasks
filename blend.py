#!/usr/bin/python3
import csv
import json
import time
from typing import List, Dict
import logging
import requests
import plotly.graph_objects as go

logging.basicConfig(level=logging.INFO)

username = "pdtpatrick"
password = "u3!WL2uC0dxu"

start_time = 3600 * 48  # 48 hours
airport = "EDDF"  # Frankfurt

# all departure flights
def departures(airport):

    # these variables will hold the departure and arrivals
    estDept = ''
    estArrival = ''

    # hese variables will hold the latitude and longitude cordinates
    depart_lat = ''
    depart_lon = ''
    arrival_lat = ''
    arrival_lon = ''

    try:
        url = f'https://opensky-network.org/api/flights/departure?airport={airport}&begin=1517227200&end=1517230800'
        response = requests.get(url)
        res = response.json() # pass data as json

        tempList = []
        newList = []
    #     fetchedData = call_api(airport)
    #     logging.info('The data is {fetchedData}')
        
        print('previous list length :' + str(len(res)))
        # loop through the data
        for f in res:
            # store the estDepartureAirport and estArrivalAirport values
            deptarture_airport = f['estDepartureAirport']
            arrival_airport = f['estArrivalAirport']

            # append to data to the tempList
            tempList.append(
                {deptarture_airport: arrival_airport}
            )

            # loop through the dictionary in the tempList
        for pairs in tempList:
            # check if pairs doesn't exists and append them to the newList
            if pairs not in newList:
                newList.append(pairs) 

        print('new list length :' + str(len(newList)))

        # read from the csv file
        with open('./airports.csv', mode='r') as csvfile:
            # reading the csv file
            content = csv.reader(csvfile)
            
            estDept = ''
            estArrival = []
            tempLat = []
            tempLon = []
            finalLat = []
            finalLon = []
            # loop through the new list
            for pairs in newList:
                # loop through the items of the dict
                for key,val in pairs.items():
                    estDept = key
                    estArrival.append(val)
                    # print(f'key:{key} -> value:{val}')

            # loop through the csvfile
            for con in content:
                for est in estArrival:
                    # check if departure airport exists in csv
                    if con[5] == estDept:
                        print('dept found: '+ str(con[5]))
                        # depart_lat = con[6]
                        # depart_lon = con[7]
                        tempLat.append(con[6])
                        tempLon.append(con[7])

                        # for pairs in tempLat:
                        #     if pairs not in finalLat:
                        #         finalLat.append(pairs)
                                
                        # for pairs in tempLon:
                        #     if pairs not in finalLon:
                        #         finalLon.append(pairs)

                        print('dept lat: ' + str(tempLat))
                        print('dept lon: ' + str(tempLon))
                        # print('dept lat: ' + depart_lat)
                        # print('dept lon: ' + depart_lon)

                    # check if arrival airport exist in csv
                    if con[5] == est:
                        print('est found: '+ str(con[5]))
                        # arrival_lat = con[6]
                        # arrival_lon = con[7]
                        tempLat.append(con[6])
                        tempLon.append(con[7])

                        # for pairs in tempLat:
                        #     if pairs not in finalLat:
                        #         finalLat.append(pairs)
                                
                        # for pairs in tempLon:
                        #     if pairs not in finalLon:
                        #         finalLon.append(pairs)

                        print('dept lat: ' + str(tempLat))
                        print('dept lon: ' + str(tempLon))
                        # print('arri lat: ' + arrival_lat)
                        # print('arri lon: ' + arrival_lon)

        # generating a Scattermapbox
        fig = go.Figure(go.Scattermapbox(
            mode = "markers+lines",
            lat = tempLat, # [50.8658981323,48.353802,52.5597,48.110298156738], # finalLat, # [depart_lat,arrival_lat],
            lon = tempLon, # [7.1427397728,11.7861,13.2877,16.569700241089], # finalLon, # [depart_lon,arrival_lon],

            # set the marker size
            marker = {'size': 10}
        ))


        # # update the layout
        fig.update_layout(
            margin ={'l':0,'t':0,'b':0,'r':0},
            mapbox = {
                'center': {'lon': 10, 'lat': 10},
                'style': "stamen-terrain",
                'center': {'lon': -20, 'lat': -20},
                'zoom': 1})

        # draw the map
        fig.show()

    except IndexError:
        print('--------------------------------------------------')
        print('{} is not part of opensky\'s api'.format(airport))

    
departures("EDDK")
# EDDK
# LSGG -> LHBP (found)
# EGLL -> KLAS (found)