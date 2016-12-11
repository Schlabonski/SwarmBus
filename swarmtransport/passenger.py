class SimplePassenger(object):

    """A simple object representing a passenger.
    
    The most simple passenger will only have a current position and a
    destination.
    """

    def __init__(self, start_position, destination):
       self.start_position = start_position
       self.destination = destination
