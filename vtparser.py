#!/usr/bin/python3
'''
Helper functions for getting departures
'''
from vtomatic import VtOMatic

def get_departures(stop_name, destinations=None):
    '''
    Returns departures to destination from given stop name.
    If destination is None, all departures are returned
    '''
    vtomatic = VtOMatic()
    stops = vtomatic.get_stops_by_name(stop_name)
    stop_id = None
    for stop in stops:
        if stop['name'] == stop_name:
            stop_id = stop['id']
    departure_board = vtomatic.get_departures_by_id(stop_id)
    if destinations != None:
        for departure in departure_board:
            if departure['direction'] not in destinations:
                departure_board.remove(departure)
    return departure_board

if __name__ == '__main__':
    STOP_INPUT = input('Enter stop name(or press enter for default):')
    if STOP_INPUT == '':
        STOP_INPUT = 'Vallhamra torg, Partille'
    BUS_NAME = input('Enter bus name(or press enter for default):')
    if BUS_NAME == '':
        BUS_NAME = 'SVART EXPRESS'
    INPUT_DESTINATIONS = []
    INPUT_DESTINATION = input('Enter destination(empty for all):')
    if INPUT_DESTINATION != '':
        INPUT_DESTINATIONS.append(INPUT_DESTINATION)
    else:
        INPUT_DESTINATIONS = None
    DEPARTURES = get_departures(STOP_INPUT, INPUT_DESTINATIONS)
    for dep in DEPARTURES:
        if dep['name'] == BUS_NAME:
            print(dep['sname'] + ' ' + dep['direction'] + ' '\
                    + dep['rtTime'] + '(' + dep['time'] + ')')

