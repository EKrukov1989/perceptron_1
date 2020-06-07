"""Main module for perceptron_1.

This module consists all logic of top level
"""

import tkinter as tk
from graphwindow import GraphWindow
from logwindow import LogWindow, EntryType
from controlsmanager import ControlsManager
import dataloadingutil


def __show_points(controls, graph, log):
    path = controls.get_data_path()
    error, data = dataloadingutil.load_data(path)
    if error:
        log.log_err(error)
    else:
        graph.set_points(data)
        log.add_entry('Train data was successfully loaded ' +
                      '(number of points: ' + str(len(data)) + ')')


def main():
    """Start application."""
    root = tk.Tk()

    root.wm_iconbitmap('src/images/window.ico')
    root.minsize(800, 600)
    root.state('zoomed')
    root.wm_title('perceptron_1')

    graph = GraphWindow(root)
    log = LogWindow(root)
    controls = ControlsManager(root)

    controls.set_show_button_callback(
        lambda: __show_points(controls, graph, log))

    root.mainloop()


if __name__ == '__main__':
    main()
