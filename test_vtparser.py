#!/usr/bin/python3
'''
Unittests for vtparser
'''
import unittest
from unittest.mock import MagicMock
import pickle

import vtparser
from vtomatic import VtOMatic

class TestVtparser(unittest.TestCase):
    '''
    The unit test class
    '''

    def test_departure_list(self):
        '''
        Test that the departure list
        parsing works correctly
         '''
        with open('departures.dat', 'rb') as data:
            vtomatic = VtOMatic()
            departure_data = pickle.load(data)
            vtomatic.get_departures_by_id = MagicMock(return_value=departure_data)

            destination = 'Centralstationen'
            departures = vtparser.get_departures(vtomatic, 'Vallhamra torg, Partille',
                                                 destination)
            self.assertEqual(len(departures), 0)
            destination = 'Amhult'
            departures = vtparser.get_departures(vtomatic, 'Vallhamra torg, Partille',
                                                 destination)
            self.assertEqual(len(departures), 5)
            destination = None
            departures = vtparser.get_departures(vtomatic, 'Vallhamra torg, Partille',
                                                 destination)
            self.assertEqual(len(departures), 20)

if __name__ == '__main__':
    unittest.main()
