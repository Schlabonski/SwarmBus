import random

import numpy as np

class SimplePassenger(object):

    """A simple object representing a passenger.
    
    The most simple passenger will only have a current position and a
    destination.
    """

    def __init__(self, start_position, destination):
       self.start_position = start_position
       self.destination = destination

class TraficNetwork(object):

    """A network of bus stations."""

    def __init__(self, stations=[]):
        self._stations = stations


class PassengerQueue(object):

    """A queue to manage the waiting passengers."""

    def __init__(self):
       self.waiting = []

    def put_back(self, passenger):
        self.waiting.insert(0, passenger)

    def get_next(self):
        next_passenger = self.waiting.pop(0)
        return next_passenger

    def add(passenger):
        self.waiting.append(passenger)

def initialize_random_network(n, map_size):
    """Creates a random `TraficNetwork` with `n` stations.

    :n: int
        number of stations
    :map_size: 2-tuple
        Size of map on which the stations are placed in 2d

    """
    stations = []

    for i in range(n):
        x, y = np.random.rand(2)
        x *= map_size[0]
        y *= map_size[1]
        stations.append([x,y])
    
    random_network = TraficNetwork(stations=stations)
    return random_network

def create_random_passenger(traffic_network):
    """Creates a random passenger on the given network.


    """
    start = random.choice(traffic_network._stations)
    destination = random.choice(traffic_network._stations)

    random_passenger = SimplePassenger(start, destination)

    return random_passenger
