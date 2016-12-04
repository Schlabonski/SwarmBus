from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
import numpy as np
from vispy import scene

class CityMap(object):

    """Represents the city map on which public transport can move and represents
    it as a vispy canvas."""

    def __init__(self, size, bgcolor='#cdcdcd'):
        """

        :size: 2-tuple
            size of the map in x and y direction
        :bgcolor: color
            backgroundcolor of the map

        """
        self.size = size
        self.canvas = scene.SceneCanvas(keys='interactive', size=size,
                show=True, bgcolor=bgcolor)

    def color_from_position(self,  position):
        """Returns a unique RGB color for each position on the map.

        :position: TODO
        :returns: TODO

        """
        # normalize the position on the map to a position in the colorspace
        x = position[0] / self.size[0]# / 2
        y = position[1] / self.size[1]# /2
        z = 1 - x - y

        xyz = XYZColor(x, y, z)
        rgb = convert_color(xyz, sRGBColor)
  
        rgb_tuple = (rgb.clamped_rgb_r, rgb.clamped_rgb_g, rgb.clamped_rgb_b)
        
        return rgb_tuple

class BusRepresentation(object):
    """Represents the image of the bus on the city map.

    I.e. the vispy rectangle that is drawn on the city map canvas.
    """

    def __init__(self, bus_object, canvas, color='r'):
        pos = bus_object.position
        
        self.repr = scene.Rectangle(pos=pos, height=100, width=40, color=color,
                radius=10, border_color='#545454', parent= canvas.central_widget,
                antialias=True, method='agg')
