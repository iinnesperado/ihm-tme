import pyglet
import time
import numpy
from abc import abstractmethod
import math


class Cursor:
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def update_cursor(self, deltax, deltay):
        pass


class AbsoluteCursor(Cursor):
    def __init__(
        self,
        Window,
        image="img/cursor.png",
    ):
        """Create a cursor.

        Creates a cursor, which is a sprite (see pyglet documentation) with some additions. The cursor visual can be changed by inputting any image. The selection point is considered to be 1 pixel to the right and 1 pixel to the bottom of the top left corner.
        The cursor has method draw() that is called for drawing and a method update_cursor() that is called to modify the sprite's position.
        Original behaviors of the cursor can be implemented by modifying this function.

        Arguments:
        Window = [WindowWidth, WindowHeight]: list with the size of the window where the cursor is displayed. This is useful to keep the cursor inside the window.

        Keyword Arguments:
        image = location: location is the string which gives the location of the cursor image that is used for the cursor sprite.
        """
        self.wwidth, self.wheight = Window
        image = pyglet.image.load(image)

        ### These values can be found by manually comparing the position of a sprite and the cursor coordinates. Maybe a cleaner solution could be implemented in the future
        image.anchor_x = int(1)
        image.anchor_y = int(image.height - 1)

        self.width = image.width
        self.height = image.height
        self.sprite = pyglet.sprite.Sprite(image, x=500, y=500)
        self.buffer_x = []
        self.buffer_y = []
        self.buffer_t = []

    def draw(self):
        """Draws the cursor"""
        self.sprite.draw()

    def update_cursor(self, deltax, deltay):
        """Updates the cursor position from received deltas"""
        deltax = deltax
        deltay = deltay

        self.sprite.x = numpy.clip(
            self.sprite.x + deltax,
            int(self.width / 2),
            self.wwidth + int(self.width / 2),
        )
        self.sprite.y = numpy.clip(
            self.sprite.y + deltay,
            -int(self.height / 2),
            self.wheight - int(self.height / 2),
        )

        self.buffer_x.append(self.sprite.x)
        self.buffer_y.append(self.sprite.y)
        self.buffer_t.append(time.time())


class PolyCursor(Cursor):
    def __init__(self, cursors, active=0):
        self.cursors = cursors
        self.active = active

    def __getattr__(self, name):
        return getattr(self.cursors[self.active], name)

    def draw(self):
        for cursor in self.cursors:
            cursor.draw()

    def update_cursor(self, deltax, deltay):
        for cursor in self.cursors:
            cursor.update_cursor(deltax, deltay)

class ConstantCDGainCursor(Cursor):
    """Cursor with constant control-display gain"""
    
    def __init__(self, Window, gain=1.0, image="img/cursor.png"):
        """
        Cursor with constant control-display gain.
        
        Args:
            Window: [width, height] of the window
            gain: Constant gain factor (k in g(u) = k)
            image: Path to cursor image file
        """
        self.wwidth, self.wheight = Window
        self.gain = gain
        
        image = pyglet.image.load(image)
        image.anchor_x = int(1)
        image.anchor_y = int(image.height - 1)

        self.width = image.width
        self.height = image.height
        self.sprite = pyglet.sprite.Sprite(image, x=500, y=500)
        self.buffer_x = []
        self.buffer_y = []
        self.buffer_t = []
        
    def update_cursor(self, deltax, deltay):
        """
        Update cursor position with constant gain applied.
        
        Args:
            deltax: Change in x (device coordinates)
            deltay: Change in y (device coordinates)
        """
        deltax *= self.gain
        deltay *= self.gain

        self.sprite.x = numpy.clip(
            self.sprite.x + deltax,
            int(self.width / 2),
            self.wwidth + int(self.width / 2),
        )
        self.sprite.y = numpy.clip(
            self.sprite.y + deltay,
            -int(self.height / 2),
            self.wheight - int(self.height / 2),
        )

        self.buffer_x.append(self.sprite.x)
        self.buffer_y.append(self.sprite.y)
        self.buffer_t.append(time.time())
        
    def draw(self):
        """Draw the cursor"""
        self.sprite.draw()

class CustomCursor(Cursor):
    def __init__(self, Window, c=1.0, r=1.0, image="img/cursor.png"):
        """
        Cursor with power-law transfer function g(u) = c * u^r
        
        Args:
            Window: [width, height] of the window
            c: Scaling coefficient
            r: Exponent
            image: Path to cursor image file
        """
        self.wwidth, self.wheight = Window
        self.c = c
        self.r = r
        
        image = pyglet.image.load(image)
        image.anchor_x = int(1)
        image.anchor_y = int(image.height - 1)
        
        self.width = image.width
        self.height = image.height
        self.sprite = pyglet.sprite.Sprite(image, x=500, y=500)
        self.buffer_x = []
        self.buffer_y = []
        self.buffer_t = []

    def draw(self):
        """Draw the cursor (same as AbsoluteCursor)"""
        self.sprite.draw()

    def update_cursor(self, deltax, deltay):
        """
        Update cursor position with power-law transfer function applied.
        
        Args:
            deltax: Change in x (device coordinates)
            deltay: Change in y (device coordinates)
        """
        # Calculate movement speed (u)
        speed = math.sqrt(deltax**2 + deltay**2)
        
        # Apply transfer function g(u) = c * u^r
        if speed > 0:  # Avoid division by zero
            gain = self.c * (speed ** (self.r - 1))
            deltax *= gain
            deltay *= gain

        # Update position with bounds checking
        self.sprite.x = numpy.clip(
            self.sprite.x + deltax,
            int(self.width / 2),
            self.wwidth + int(self.width / 2),
        )
        self.sprite.y = numpy.clip(
            self.sprite.y + deltay,
            -int(self.height / 2),
            self.wheight - int(self.height / 2),
        )

        # Log movement data
        self.buffer_x.append(self.sprite.x)
        self.buffer_y.append(self.sprite.y)
        self.buffer_t.append(time.time())