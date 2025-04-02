from window import EXPWINDOW
import pyglet
import math


window2 = EXPWINDOW(
    "FITTS2D", 15, caption="Expérience", resizable=False, fullscreen=True
)
pyglet.clock.schedule_interval(window2.update, window2.frame_rate)
pyglet.app.run()
