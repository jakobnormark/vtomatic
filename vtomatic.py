#!/usr/bin/python3
'''
This file contains the class VtOMatic and the constants used by the class
'''
import base64
import json
import configparser
import os
import sys
import time
import requests

TOKEN_URL = 'https://api.vasttrafik.se/token'
API_BASE_URL = 'https://api.vasttrafik.se/bin/rest.exe/v2'

class VtOMatic:
    '''
    VtOMatic is a class that fetches information from
    Vasttrafik API "Reseplaneraren" v2
    '''
    def __init__(self):
        '''
        Constructor. It initializes the authentication token
        '''
        self._key = None
        self._secret = None
        self._token = None

        # Get & set key and secret
        self.init_credentials()

        # Get & set the access token
        self.init_token()

    def init_credentials(self):
        '''
        Retreive and set key and secret from ~/.vtomaticrc
        '''
        config_file = os.path.expanduser('~') + '/.vtomaticrc'
        config = configparser.ConfigParser()
        files_read = config.read(config_file)
        if len(files_read) == 0:
            sys.exit('Could not read config file: ' + config_file)
        api_credentials = config['api_credentials']
        self._key = api_credentials['key']
        self._secret = api_credentials['secret']

    def init_token(self):
        '''
        get_token returns an access token obtained with the
        key and secret
        '''
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': 'Basic ' + base64.b64encode((self._key + ':' \
            + self._secret).encode()).decode()
        }
        data = {'grant_type': 'client_credentials'}

        response = requests.post(TOKEN_URL, data=data, headers=headers)
        obj = json.loads(response.content.decode('UTF-8'))
        self._token = obj['access_token']

    def get_departures_by_id(self, stop_id, query_params=None, verbose=False):
        '''
        Requests all coming departures from a stops id
        Returns a list with departures or None
        '''
        departures = self.get('/departureBoard?id=' + stop_id + '&date=' + \
                     time.strftime("%Y-%m-%d") + '&time=' + \
                     time.strftime("%H:%M"), query_params)
        if verbose:
            print(departures)
        return departures['DepartureBoard']['Departure']

    def get_stops_by_name(self, query, query_params=None):
        '''
        Requests stops by name. Returns a list with stops or None
        '''
        return_data = None
        stops = self.get('/location.name?input=' + query, query_params)
        if stops is not None:
            return_data = stops['LocationList']['StopLocation']
        return return_data

    def get(self, endpoint, query_params):
        '''
        Request builder function. It returns a result in json, or None
        '''
        url = API_BASE_URL + endpoint + '&format=json'
        if query_params is not None:
            for key in query_params:
                url += '&' + key + '=' + query_params[key]
        headers = {
            'Authorization': 'Bearer ' + self._token
        }
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            return json.loads(res.content.decode('UTF-8'), 'UTF-8')
        else:
            return None

