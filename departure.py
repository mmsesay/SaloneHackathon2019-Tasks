#!/usr/bin/python3
import csv
import json
import time
import requests
import plotly.graph_objects as go

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
        res = response.json()[0] # pass data as json

        # save the reterived data
        estDept = res['estDepartureAirport']
        estArrival = res['estArrivalAirport']

        # check if the estimated arrival retrived was empty
        if estArrival == None:
            print('--------------------------------------------------')
            print('{} airport doesn\'t have an estimated arrival\
        so the marker will just be at the departure airport'.format(estDept))

        print('Departure AirPort: {} - Arrival Airport: {}'.format(estDept,estArrival))
        print('--------------------------------------------------')

        # read from the csv file
        with open('./airports.csv', mode='r') as csvfile:
            # reading the csv file
            content = csv.reader(csvfile)

            # loop through the csvfile
            for con in content:
                # check if departure airport exists in csv
                if con[5] == estDept:
                    print('dept found: '+ str(con[5]))
                    depart_lat = con[6]
                    depart_lon = con[7]
                    print('dept lat: ' + depart_lat)
                    print('dept lon: ' + depart_lon)

                # check if arrival airport exist in csv
                if con[5] == estArrival:
                    print('est found: '+ str(con[5]))
                    arrival_lat = con[6]
                    arrival_lon = con[7]
                    print('arri lat: ' + arrival_lat)
                    print('arri lon: ' + arrival_lon)

        # generating a Scattermapbox
        fig = go.Figure(go.Scattermapbox(
            mode = "markers+lines",
            lat = [depart_lat,arrival_lat],
            lon = [depart_lon, arrival_lon],

            # set the marker size
            marker = {'size': 10}
        ))


        # update the layout
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

    
departures("LSGG")
# EDDK
# LSGG -> LHBP (found)
# EGLL -> KLAS (found)