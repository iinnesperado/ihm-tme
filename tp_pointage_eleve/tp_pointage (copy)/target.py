import math


class TARGET:
    def __init__(self, target_type = "circle", scale = 10, posx = 0, posy= 0, smoothness = 100, state = "distractor"):
        """Defines a target.

        Creates a target using pyglet/OpenGL commands. For now only circular targets are implemented, and the color is fixed.

        Keyword Arguments:
        target_type = string: The name of the target. For now only the name 'circle' is implemented; more might be used in the future.
        scale = int: Factor that determines the size of the target. For the circle, scale determines its radius.
        posx, posy = int, int: Position of the reference point of the target in pixels. For the circle, the reference point is its center.
        smoothness = int: Number that is used to draw enough vertexes in openGL. May be tuned down if the program starts slowing down, or tuned up if the shapes look irregular.
        state = string: property of the target. For now, only the state distractor is implemented, which only implies a blueish color.
        """
        if target_type== 'circle':
            circle_vertex, circle_color, circle_index = self.create_disk(posx, posy, scale, smoothness, state = "distractor")
            self.v_list_verts = circle_vertex
            self.v_list_colors = circle_color
            self.v_list_indx = circle_index

        ### Implement other target types
        else:
            pass

    def create_disk(self, posx, posy, radius, smoothness, state = "distractor"):
        """ Creates a Vertex, Colors and Index lists for a disk.

        scale = int: Factor that determines the size of the target. For the circle, scale determines its radius.
        posx, posy = int, int: Position of the reference point of the target in pixels. For the circle, the reference point is its center.
        smoothness = int: Number that is used to draw enough vertexes in openGL. May be tuned down if the program starts slowing down, or tuned up if the shapes look irregular.
        state = string: property of the target. For now, only the state distractor is implemented, which only implies a blueish color.
        """
        _vertexes = [posx, posy]
        _colors = []
        if state == "distractor":
            _color_sample = [66, 135, 245, 255]
        else:
            _color_sample = [0,0,0,255]
        for i in range(int(smoothness)+1):
            angle = math.radians(float(i)/smoothness * 360.0)
            x = radius*math.cos(angle) + posx
            y = radius*math.sin(angle) + posy
            _vertexes += [x,y]
            _colors += _color_sample
        ## Add degenerate vertices
        _vertexes = [radius + posx, posy] + _vertexes
        _colors += _color_sample
        _colors += _color_sample
        ## Add indices
        _indices = []
        for enum in range(int(smoothness)+1):
            _indices.append(0)
            _indices.append(enum)
            _indices.append(enum + 1)
        return _vertexes, _colors, _indices
