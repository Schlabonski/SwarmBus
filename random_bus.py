from swarmtransport.representations import CityMap, BusRepresentation 
from swarmtransport.publictransport import SimpleBus, DecisiveBus
import swarmtransport.passenger as ps

from vispy import app, scene
from vispy.ext.six import next
import vispy.io

from vispy.visuals.transforms.linear import AffineTransform

import numpy as np

# define a rotation transformation
def rotation_matrix(deg):
    pass

# initialize a citymap and a traffic network
citymap = CityMap(size=(1000, 800))
traffic_network = ps.initialize_random_network(15, citymap.size)


busses = []
bus_representations = []
bus_positions = []
n_buses = 15

# initialize the busses and their representations
for i in range(n_buses):
    position = np.random.rand(2) * np.array(citymap.size)
    destination = np.random.rand(2) * np.array(citymap.size)

    bus = DecisiveBus(x_init=position, v_max=40, a_max=20)
    bus_position = bus.drive(destination, dt=0.1)

    bus_color = citymap.color_from_position(bus.position)
    bus_repr = BusRepresentation(bus, canvas=citymap.canvas, color=bus_color)

    bus_repr.translate_rotate(bus.position, bus.phi/2/np.pi * 360)

    busses.append(bus)
    bus_representations.append(bus_repr)
    bus_positions.append(bus_position)

n = 0
def update(event):
    global n
    for i in range(n_buses):
        bus = busses[i]
        bus_repr = bus_representations[i]
        bus_position = bus_positions[i]
        try:
            x,v = next(bus_position)

            new_color = citymap.color_from_position(x)
            bus_repr.repr.color = new_color
            
            # adapt the direction and position of the bus
            bus_repr.translate_rotate((x[0], x[1]), bus.phi/2/np.pi * 360)

        except StopIteration:
            random_x = np.random.random(2) * np.array(citymap.size)
            bus_positions[i] = bus.drive(random_x, dt=0.1)
            x = bus.position

    citymap.canvas.update()
    #image = citymap.canvas.render()
    #vispy.io.write_png('movie/shot{0}.png'.format(n), image)
    n += 1

timer = app.Timer(0.001, connect=update, start=True)

if __name__ == '__main__':
    citymap.canvas.app.run()
