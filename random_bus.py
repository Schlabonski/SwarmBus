from swarmtransport.representations import CityMap, BusRepresentation 
from swarmtransport.publictransport import SimpleBus

from vispy import app, scene
from vispy.ext.six import next
import vispy.io

from vispy.visuals.transforms.linear import AffineTransform

import numpy as np

# define a rotation transformation
def rotation_matrix(deg):
    pass

citymap = CityMap(size=(1000, 800))

busses = []
bus_representations = []
bus_positions = []
n_buses = 15
for i in range(n_buses):
    position = np.random.rand(2) * np.array(citymap.size)
    destination = np.random.rand(2) * np.array(citymap.size)

    bus = SimpleBus(x_init=position, v_max=40, a_max=20)
    bus_position = bus.drive(destination, dt=0.1)

    bus_color = citymap.color_from_position(bus.position)
    bus_repr = BusRepresentation(bus, canvas=citymap.canvas, color=bus_color)
    
    rotation = scene.AffineTransform()
    rotation.translate((-bus.position[0],-bus.position[1],0))
    rotation.rotate(bus.phi, (0,0,1))
    rotation.translate((bus.position[0], bus.position[1], 0))
    bus_repr.repr.transform *= rotation

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
            bus_repr.repr.pos = (x[0], x[1])

            new_color = citymap.color_from_position(x)
            bus_repr.repr.color = new_color
            
            # adapt the direction of the bus
            bus_repr.repr.transform = AffineTransform()

            rotation = AffineTransform()
            rotation.translate((-x[0], -x[1], 0))
            rotation.rotate(bus.phi/2/np.pi * 360, (0,0,1))
            rotation.translate((x[0], x[1], 0))

            bus_repr.repr.transform *= rotation

        except StopIteration:
            random_x = np.random.random(2) * np.array(citymap.size)
            bus_positions[i] = bus.drive(random_x, dt=0.1)
            x = bus.position



    citymap.canvas.update()
    image = citymap.canvas.render()
    vispy.io.write_png('movie/shot{0}.png'.format(n), image)
    n += 1
    

timer = app.Timer(0.001, connect=update, start=True)

if __name__ == '__main__':
    citymap.canvas.app.run()
