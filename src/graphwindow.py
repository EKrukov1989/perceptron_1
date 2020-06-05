"""Module for GraphWindow-class."""

import globals
import tkinter as tk


class GraphWindow():
    """The class incapsulated all logic for graph window.

    It creates GUI-elements, draw and redraw data
    """

    __graph_canvas = None
    __points = None
    __line = None

    def __redraw(self):
        """Redraw all in graph window."""
        w = self.__graph_canvas.winfo_width()
        h = self.__graph_canvas.winfo_height()

        # sx & sy - means screen coordinates
        def sx(x): return 0.5 * w * (1 + x)
        def sy(y): return 0.5 * h * (1 - y)

        self.__graph_canvas.delete('axis')
        self.__graph_canvas.delete('points')
        self.__graph_canvas.delete('line')

        # draw axis
        self.__graph_canvas.create_line(sx(-1), sy(0), sx(1), sy(0),
                                        tags='axis', fill='blue')
        self.__graph_canvas.create_line(sx(0), sy(-1), sx(0), sy(1),
                                        tags='axis', fill='red')
        # draw points
        if self.__points is not None:
            for pt in self.__points:
                x, y = sx(pt[0]), sy(pt[1])
                sh = 4  # shift
                self.__graph_canvas.create_oval((x-sh, y-sh, x+sh, y+sh),
                                                tags='points', fill='green',
                                                outline='green')

        # draw line
        if self.__line is not None:
            for i in range(1, len(self.__line)):
                x0, x1 = sx(self.__line[i-1][0]), sx(self.__line[i][0])
                y0, y1 = sy(self.__line[i-1][1]), sy(self.__line[i][1])
                self.__graph_canvas.create_line(x0, y0, x1, y1, width=2,
                                                tags='line', fill='black')

    def __init__(self, parent_frame):
        """Create GUI-elements and attach them to parent."""
        graph_frame = tk.Frame(parent_frame)
        graph_frame.place(anchor='nw', relwidth=0.5, relheight=0.5)
        graph_frame_inner = tk.Frame(graph_frame)
        graph_frame_inner.pack(expand=True, fill='both',
                               padx=(2*globals.FRAME_PAD, globals.FRAME_PAD),
                               pady=(2*globals.FRAME_PAD, globals.FRAME_PAD))
        graph_frame['bg'] = globals.BG_COLOR
        graph_frame_inner['bg'] = globals.BG_COLOR

        self.__graph_canvas = tk.Canvas(graph_frame_inner)
        self.__graph_canvas['bg'] = 'white'
        self.__graph_canvas['highlightthickness'] = 0
        self.__graph_canvas.place(anchor='nw', relwidth=1.0, relheight=1.0)

        self.__graph_canvas.bind('<Configure>', lambda e: self.__redraw())

    def set_points(self, points_array):
        """Set 2d-array of points.

        Each point will be drawn as circle in graph window.
        All coordinates must be in the nterval [-1;1]
        """
        self.__points = points_array
        self.__redraw()

    def set_line(self, line_array):
        """Set 2d-array of points for line.

        This points will be used for drawing line in graph window.
        All coordinates must be in the nterval [-1;1]
        """
        self.__line = line_array
        self.__redraw()
