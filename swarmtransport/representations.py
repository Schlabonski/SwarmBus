from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
import numpy as np
from vispy import scene
from vispy.visuals.transforms.linear import AffineTransform

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
    
    def translate(self, pos):
        """Translates the representation to the  new position `pos`.

        :pos: 2d array_like

        """
        self.repr.repr.pos = (pos[0], pos[1])

    def translate_rotate(self, pos, angle_abs):
        """Translates and rotates the BusRepresentation object.

        :angle_abs: absolute rotation angle in degrees
        :pos: 2d arra_like of position

        """
        transform = AffineTransform()

        # first we need to transform the representation to the origin
        current_pos = self.repr.pos

        transform.translate((-current_pos[0], -current_pos[1], 0))

        # in the origin, rotate the representation around the z-axis
        transform.rotate(angle_abs, (0,0,1))

        # translate the representation to the new position
        transform.translate((pos[0], pos[1], 0))

        # multiply the transformation to the previous one
        self.repr.transform = transform

