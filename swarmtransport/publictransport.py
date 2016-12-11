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

        # update the angle of the bus with respect to e_x
        phi = np.arctan2(direction[1], direction[0])
        self.phi = phi + np.pi/2

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

class DecisiveBus(SimpleBus):

    """A decisive bus can pick passengers and decide whether it picks one or
    not."""

    def __init__(self, max_route_length=100, **kwargs):
        super().__init__(**kwargs)
        self.max_route_length = max_route_length
        self.passengers = [] # should this be a list or another structure?

    def pick_passenger(self, passenger):
        """Adds a passenger to the planned route.

        This function will check whether the minimum elongation of the planned
        route by taking a passenger exceeds the maximum allowed route length.

        :passenger: an instance of passenger.SimplePassenger

        """
        route = self.planned_route
        
        # no passengers yet? Go and get some!
        if len(route) == 0:
            route.append(passenger.start_position)
            route.append(passenger.destination)
            self.passengers.append(passenger)
            return


        def find_minimum_elongation(route, position):
            """Returns the optimal elongation and position where to insert
            `position` into `route`."""
            # find the elongation of the route for every possible insertion of
            # `position` into `route`
            vector_to_position = route - position

            direct_distance = np.sqrt(np.sum((route[:-1] - route[1:])**2,
                axis=1))
            deviation_distance = np.sqrt(np.sum(vector_to_position[:-1]**2,axis=1)) \
                              + np.sqrt(np.sum(vector_to_position[1:]**2, axis=1))

            elongation = deviation_distance - direct_distance

            # find minimum elongation and its position
            elong = np.min(elongation)
            min_index = np.argmin(elongation)

            # is this worse than just inserting the position at the end?
            dist_from_end = np.sqrt(np.sum((route[-1] - position)**2))
            if dist_from_end < elong:
                return dist_from_end, -1

            return elong, min_index+1

        # calculate the current total length of the route
        route_array = np.asarray(route)
        start_position = np.asarray(passenger.start_position)
        destination = np.asarray(passenger.destination)

        current_length_of_route = np.sum(np.linalg.norm(route_array[:-1]-route_array[1:], axis=1))

        # find the best position to pick up the passenger
        elongation, min_indx = find_minimum_elongation(route_array, start_position)

        # does this elongate the route too much?
        if current_length_of_route + elongation > self.max_route_length:
            return

        route.insert(min_indx, passenger.start_position)

        # check whether the destination can be inserted AFTER the start without elongating the
        # route beyond the given maximum length
        new_route_array = np.asarray(route)
        if min_indx == -1:
            elongation2 = np.linalg.norm(start_position-destination)
            min_indx2 = -1
        else:
            elongation2, min_indx2 = find_minimum_elongation(new_route_array[min_indx:], destination)

        final_length = current_length_of_route + elongation + elongation2
        if final_length > self.max_route_length:
            # remove start point from route
            route.pop(min_indx)
            return

        route.insert(min_indx2, passenger.destination)

