import pyglet
from pyglet.window import key, FPSDisplay
import sys
import itertools
import math
import numpy
import random
import time
import subprocess

from cursor import AbsoluteCursor, PolyCursor, ConstantCDGainCursor, CustomCursor


from target import TARGET


class EXPWINDOW(pyglet.window.Window):

    def __init__(self, XP_type, ntrials, *args, load=False, **kwargs):

        FPSRATE = 1 / 60
        ### Get all input params
        super().__init__(*args, **kwargs)
        self.XP_type = XP_type
        self.ntrials = ntrials

        self.trial_limit = 20

        self.p_number = 1

        self.load = load

        ## Set some KEYWORDS based on XP_type
        if XP_type == "FITTS2D":
            self.XP_INDICATOR = 1
            self.NOTIF_TEXT = "Press D to start."
            self.SKIP_TRIAL = 2
        else:
            print("Error, XP_type not known. Exiting")
            exit()

        ## Prepare the layout
        pyglet.gl.glClearColor(0.8, 0.8, 0.8, 1)
        self.clear()
        self.frame_rate = FPSRATE
        self.fps_display = FPSDisplay(self)
        self.fps_display.fontsize = 10

        ## Use virtual cursor only
        self.set_exclusive_mouse()

        ## Set Batch for background
        self.batch = pyglet.graphics.Batch()
        self.background_batch = pyglet.graphics.OrderedGroup(0)

        self.trial_count = 0
        self.local_trial_count = 0

        ## Load XP Design parameters
        if self.load:
            self.load_design("design_fitts2D.csv")
        else:
            conditions = [[9, 350]]
            self.conditions = iter(conditions)

        ## Prepare instructions
        self.notif = pyglet.text.Label(
            self.NOTIF_TEXT,
            font_name="Times New Roman",
            font_size=25,
            x=self.width / 2,
            y=self.height / 3,
            anchor_x="center",
            anchor_y="center",
            width=int(0.9 * self.width),
            multiline=True,
        )

        ## Open CSV file for output
        u = "[START_EXPERIMENT, Participant {}, Date = {}, Condition:D-ID-W-Ntrials]".format(
            self.p_number, time.ctime()
        )
        output_file = (
            "output/XP_" + str(self.XP_INDICATOR) + "_P{}.csv".format(self.p_number)
        )
        with open(output_file, "w") as tmp_f:
            tmp_f.write(u.strip("[]") + "\n")

        print("Opening" + output_file)
        ## Initialize cursor
        window = [self.width, self.height]
        self.cursor = AbsoluteCursor(window)
        # self.cursor = ConstantCDGainCursor(window, gain=1.0)
        # Choix de 1 pour la valeur du gain car plus que ça le cursor est trop rapide 
        # et pour une valeur inférieur trop lente
        # self.cursor = CustomCursor(window, c=2.0, r=0.9)

        abs_cursor = AbsoluteCursor(window)
        cdgain_cursor = ConstantCDGainCursor(window, gain=1.0)  
        custom_cursor = CustomCursor(window, c=2.0, r=0.9)
        self.cursor = PolyCursor([abs_cursor, cdgain_cursor, custom_cursor])


        ## Initialize Labels
        self.counting_string = pyglet.text.Label(
            "",
            font_name="Times New Roman",
            font_size=25,
            x=self.width / 2,
            y=self.height / 3,
            anchor_x="center",
            anchor_y="center",
        )

        ## Prepare target image
        image_truetarget = "img/target.png"
        img_target = pyglet.image.load(image_truetarget)
        img_target.anchor_x = int(img_target.width / 2)
        img_target.anchor_y = int(img_target.height / 2)
        self.sprite_trgt = pyglet.sprite.Sprite(img_target)

        ## Prepare helper image
        image_helper = "img/helper.png"
        img_helper = pyglet.image.load(image_helper)
        img_helper.anchor_x = int(img_helper.width / 2)
        img_helper.anchor_y = int(img_helper.height / 2)
        self.sprite_helper = pyglet.sprite.Sprite(img_helper)

        ## Initialize Target management variables
        self.active = None
        self.helper = None
        self.cover = 0
        ## Technique management
        # self.update_tech("Gnome default")
        self.update_tech("Flat")

        ## Init finished, greet Participant
        print("Welcome Participant {}; \n Get ready.".format(self.p_number))

    def load_design(self, _file):
        ### expects a list of lists (Nblocks x 2) ie. [[factor 1 level, factor2 level], [factor 1 level, factor2 level],[factor 1 level, factor2 level], ..., [factor 1 level, factor2 level]]
        conditions = []
        cond = []
        with open(_file, "r") as tmp_f:
            tmp_f.readline()
            for n, _line in enumerate(tmp_f):
                _words = _line.strip().split(",")
                if self.p_number is not int(float(_words[1])):
                    pass
                else:
                    if _words[4] == "F1":
                        cond.append(4)
                    elif _words[4] == "F2":
                        cond.append(9)
                    elif _words[4] == "F3":
                        cond.append(25)
                    else:
                        print("wrong design")
                        exit()
                    if _words[5] == "S1":
                        cond.append(150)
                    elif _words[5] == "S2":
                        cond.append(350)
                    else:
                        print("wrong design")
                        exit()
                    conditions.append(cond)
                    cond = []

        if not conditions:
            print("Did not find conditions for this participant, exiting")
            exit()
        else:
            self.conditions = iter(conditions)
            print(conditions)

    def start_block(self):
        self.notif.text = ""
        self.local_trial_count = -self.SKIP_TRIAL
        print("start block")
        try:
            r, R, N = *next(self.conditions), self.ntrials
            self.W, self.D, self.N = r, R, N
            ID = math.log(1 + R / r, 2)
            self.targets = self.init_grid(self.XP_type, R, r, N)
            self.target_sequence = iter(self.get_target_sequence(self.targets, N))
            output_file = (
                "XP_" + str(self.XP_INDICATOR) + "_P{}.csv".format(self.p_number)
            )
            u = ("Condition", str(R), str(ID), str(r), str(N))
            u = ",".join(u) + "\n"
            with open("output/" + output_file, "a") as tmp_f:
                tmp_f.write(u)
        except StopIteration:
            self.end_experiment()

    def update_tech(self, technique):
        # Only for Linux + Gnome
        # try adapting to your system for convenience, otherwise you can manually turn off the transfer function
        # ========================
        self.technique = technique
        if self.technique == "Gnome default":
            process = subprocess.run(
                'gsettings set org.gnome.desktop.peripherals.mouse accel-profile "default"'.split()
            )
        else:
            process = subprocess.run(
                'gsettings set org.gnome.desktop.peripherals.mouse accel-profile "flat"'.split()
            )

    def init_grid(self, type="FITTS2D", *args):
        ### Params that may need to be adapted or may be hard coded. (?)
        _smoothness = 20

        self.grid_type = type
        targets = []

        if type == "FITTS2D" or type == "FITTS2D-training":
            R_layout, r_target, N = args
            if 2 * (R_layout + r_target) > self.height:
                print("Layout too large, adapting Radius outer circle")
                R_layout = (self.height - 2 * r_target) / 2
            for i in range(N):
                _alpha = 2 * math.pi / N * i
                px = R_layout * math.cos(_alpha) + self.width / 2
                py = R_layout * math.sin(_alpha) + self.height / 2
                _target = TARGET(
                    target_type="circle",
                    scale=r_target,
                    posx=px,
                    posy=py,
                    smoothness=_smoothness,
                    state="distractor",
                )
                self.batch.add_indexed(
                    _smoothness + 3,
                    pyglet.gl.GL_TRIANGLES,
                    self.background_batch,
                    _target.v_list_indx,
                    ("v2f/static", _target.v_list_verts),
                    ("c4B/static", _target.v_list_colors),
                )
                targets.append([px, py, r_target])

        print("initialized")
        return targets

    def get_target_sequence(self, targets, ntrials):
        #### ntrials given as input, n_trials is fixed at 20
        _type = self.XP_type
        if _type == "FITTS2D" or _type == "FITTS2D-training":
            u = []
            for i in range(math.ceil(ntrials / 2)):
                u.append(i % ntrials)
                u.append((i + math.ceil(ntrials / 2)) % ntrials)
            return [targets[i] for i in u]

    def set_target(self, posx, posy, radius):
        self.sprite_trgt.update(scale=radius / 95)
        if radius < 3 and self.XP_type != "Gauss2D":
            self.helper = 1
            self.sprite_helper.x = posx
            self.sprite_helper.y = posy
        else:
            self.helper = None
        self.sprite_trgt.x = posx
        self.sprite_trgt.y = posy
        self.active = self.sprite_trgt

    def do_pause(self):
        self.local_trial_count = 0
        self.counting_string.text = ""
        self.cover = 1
        self.notif.text = "Press C to continue. First trial doesn't count"

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.update_tech("Gnome default")
            self.close()

        if symbol == key.D and not self.active:
            print("starting experiment")
            if self.trial_limit > self.ntrials:
                self.counting_string.text = "Trial {}/{} ".format(
                    self.trial_count, self.ntrials - self.SKIP_TRIAL
                )
            else:
                self.counting_string.text = "Trial {}/{} \t  ({}/{})".format(
                    self.local_trial_count,
                    self.trial_limit,
                    self.trial_count,
                    self.ntrials,
                )
            self.start_block()
            print("block started")
            self._target = next(self.target_sequence)
            self.set_target(*self._target)
        if symbol == key.ENTER or symbol == key.RETURN:
            self.notif.text = ""
            self.start_block()
            print("block started")
            try:
                self._target = next(self.target_sequence)
                self.set_target(*self._target)
            except StopIteration:
                self.end_experiment()

        if symbol == key.C:
            self.notif.text = ""
            self.local_trial_count = -self.SKIP_TRIAL
            self.cover = 0

    def on_mouse_motion(self, x, y, dx, dy):
        self.cursor.update_cursor(dx, dy)

    def on_target(self, x, y):
        px, py, r = self._target
        if ((px - x) ** 2 + (py - y) ** 2) < 2 * r**2 + 4:
            return 1
        else:
            return 0

    def on_mouse_press(self, x, y, button, modifiers):
        try:
            x = self.cursor.sprite.x
            y = self.cursor.sprite.y
            if self.on_target(x, y):
                if self.local_trial_count > 0:
                    self.log()
                self.cursor.buffer_x = []
                self.cursor.buffer_y = []
                self.cursor.buffer_t = []
                self.trial_count += 1
                self.local_trial_count += 1
                if self.trial_limit > self.ntrials:
                    self.counting_string.text = "Trial {}/{} ".format(
                        self.local_trial_count, self.ntrials - self.SKIP_TRIAL
                    )
                else:
                    self.counting_string.text = "Trial {}/{} \t  ({}/{})".format(
                        self.local_trial_count,
                        self.trial_limit,
                        self.trial_count,
                        self.ntrials,
                    )
                if self.local_trial_count >= self.trial_limit:
                    self.do_pause()
                try:
                    self._target = next(self.target_sequence)
                    self.set_target(*self._target)
                except StopIteration:
                    self.end_block()
                if self.XP_type == "Gauss2D":
                    self.cursor.sprite.x = random.gauss(self.width / 2, 150)
                    self.cursor.sprite.y = random.gauss(self.height / 2, 150)
            else:
                print("missed target by too much")
        except AttributeError:
            pass

    def on_mouse_release(self, x, y, button, modifiers):
        self.cursor.buffer_x.append(self.cursor.sprite.x)
        self.cursor.buffer_y.append(self.cursor.sprite.y)
        self.cursor.buffer_t.append(time.time())

    def end_block(self):
        self.batch = pyglet.graphics.Batch()
        self.active = None

        self.counting_string.text = ""
        self.notif.text = (
            "You Finished this Block. Take a rest and press ENTER when ready"
        )
        print("End of block")

    def end_experiment(self):
        self.notif.text = "End of Experiment " + str(self.XP_INDICATOR)
        print("end of experiment")
        output_file = "XP_" + str(self.XP_INDICATOR) + "_P{}.csv".format(self.p_number)
        u = "END EXPERIMENT"
        with open("output/" + output_file, "a") as tmp_f:
            tmp_f.write(u + "\n")
        time.sleep(1)
        self.update_tech("Gnome default")
        self.close()

    def on_draw(self):
        self.clear()
        if not self.cover:
            if self.helper:
                self.sprite_helper.draw()
            self.batch.draw()
            self.counting_string.draw()
            if self.active:
                self.active.draw()

        self.fps_display.draw()
        if self.notif.text:
            self.notif.draw()
        self.cursor.draw()

    def on_close(self):
        if self.XP_type == "FITTS2D-training":
            print("closed")

    def update(self, dt):
        pass

    def log(self):
        if not hasattr(self.cursor, 'buffer_x') or len(self.cursor.buffer_x) < 2:
            return
            
        # Calculate speeds between consecutive points
        speeds = []
        distances = []
        timestamps = []
        
        for i in range(1, len(self.cursor.buffer_x)):
            dx = self.cursor.buffer_x[i] - self.cursor.buffer_x[i-1]
            dy = self.cursor.buffer_y[i] - self.cursor.buffer_y[i-1]
            dt = self.cursor.buffer_t[i] - self.cursor.buffer_t[i-1]
            
            if dt > 0:  # Avoid division by zero
                distance = math.sqrt(dx**2 + dy**2)
                speed = distance / dt
                speeds.append(speed)
                distances.append(distance)
                timestamps.append(self.cursor.buffer_t[i])
        
        if not speeds:
            return
        
        # Calculate statistics
        max_speed = max(speeds)
        min_speed = min(speeds)
        avg_speed = sum(speeds) / len(speeds)

        print(f"Logged trial {self.trial_count} - Max: {max_speed:.2f} px/s, Min: {min_speed:.2f} px/s, Avg: {avg_speed:.2f} px/s")