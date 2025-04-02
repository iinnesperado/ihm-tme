from window import EXPWINDOW
import pyglet
import math

# if __name__ == "__main__":

window2 = EXPWINDOW(
    "FITTS2D-training", 22, 25, caption="Expérience", resizable=False, fullscreen=True
)
pyglet.clock.schedule_interval(window2.update, window2.frame_rate)
pyglet.app.run()

_cond = math.floor((window2.p_number - 0.01) / 6)

if _cond == 0:
    window = EXPWINDOW(
        "FITTS2D",
        22,
        25,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "PVP2D",
        126,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "Gauss2D",
        63,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
elif _cond == 1:
    window = EXPWINDOW(
        "PVP2D",
        126,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "Gauss2D",
        63,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "FITTS2D",
        22,
        25,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
elif _cond == 2:
    window = EXPWINDOW(
        "Gauss2D",
        63,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "FITTS2D",
        22,
        25,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()
    window = EXPWINDOW(
        "PVP2D",
        126,
        20,
        window2.p_number,
        caption="Expérience",
        resizable=False,
        fullscreen=True,
    )
    pyglet.clock.schedule_interval(window.update, window.frame_rate)
    pyglet.app.run()

print("end experiment, thank you")
