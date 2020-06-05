"""Main module for perceptron_1.

This module consists all logic of top level
"""

import tkinter as tk
import json
from graphwindow import GraphWindow
from logwindow import LogWindow
from controlsmanager import ControlsManager


def main():
    """Start application."""
    root = tk.Tk()

    root.wm_iconbitmap('src/images/window.ico')
    root.minsize(800, 600)
    root.state('zoomed')
    root.wm_title('perceptron_1')

    graph_window = GraphWindow(root)
    points = [[-0.5, -0.5], [0.5, 0.5]]
    line = [[-0.4, -0.4], [0.4, 0.4]]
    graph_window.set_points(points)
    graph_window.set_line(line)

    log_window = LogWindow(root)
    log_window.add_entry('Area for log')

    controls_manager = ControlsManager(root)

    def on_show_button_click():
        print('Show button clicked!')

    controls_manager.set_show_button_callback(on_show_button_click)

    root.mainloop()


if __name__ == '__main__':
    main()
