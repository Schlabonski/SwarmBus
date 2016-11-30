import numpy as np

class SimpleBus(object):

    """A simple Bus that can drive from A to B!"""

    def __init__(self, x_init, v_init=0, v_max=.4, a_max=.1, phi=0, is_moving=False):
        self.position = np.asarray(x_init)
        self.speed = v_init
        self.phi = phi # angle between 0 and 2pi
        self.vmax = v_max
        self.a_max = a_max
        self.is_moving = is_moving
        self.planned_route = []


    def drive(self, x_1, dt):
        """This lets the bus drive from its current position to x_1.

        :x_1: array_like
            2D position of the bus
        :dt: float
            time step of iteration
        """
        self.is_moving = True

        # some local declarations of variables should speed up simulation
        x_0 = self.position
        v_0 = self.speed
        vmax = self.vmax
        a = self.a_max
        
        # calculate the direction to destination
        # angle is arcsin((y_new - y_old)/(x_new - x_old))
        difference = x_1 - x_0
        dist = np.sqrt(np.sum(difference**2))
        
        # calculate a unit vector in direction of the destination
        direction = difference / dist
        v_0 = v_0 * direction
        a = a * direction

        print('Starting at {0} with direction {1}'.format(x_0, direction))

        def move_one_step(x, v):
            x = x + v*dt
            if np.sqrt(np.sum(v**2)) < vmax:
                v = v + a*dt
            return x, v
        
        dist_old = dist
        while True:
            dist = np.sqrt(np.sum((x_0 - x_1)**2)) 
            if dist > dist_old:
                self.is_moving = False
                self.position = x_0
                self.speed = 0
                print('I arrived at {0}!'.format(x_0))
                raise StopIteration

            x_0, v_0 = move_one_step(x_0, v_0)
            dist_old = dist
            yield x_0, v_0 

        
    def add_passenger_to_route(self, pos, destination=[0,0]):
        """Adds a passenger to the planned route.

        :pos: position of the passenger
        :destination: destination of passenger

        """
        self.planned_route.append(pos)
        self.planned_route.append(destination)
