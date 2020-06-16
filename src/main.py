"""Main module for perceptron_1.

This module consists all logic of top level
"""

import tkinter as tk
import numpy
from graphwindow import GraphWindow
from logwindow import LogWindow, EntryType
from controlsmanager import ControlsManager
import dataloadingutil
from neuralnetwork import NeuralNetwork


def __load_points(controls, graph, log):
    path = controls.get_data_path()
    error, data = dataloadingutil.load_train_data(path)
    if error:
        log.log_err(error)
        return error, data
    else:
        graph.set_points(data)
        graph.set_line([])
        log.add_entry('Train data was successfully loaded ' +
                      '(number of points: ' + str(len(data)) + ')')
        return error, data


def __launch(controls, graph, log):
    data_error, data = __load_points(controls, graph, log)
    if data_error:
        return  # error already logged

    config_path = controls.get_configuration_path()
    config_error, config = dataloadingutil.load_configuration(config_path)
    if config_error:
        log.log_err(config_error)
        return

    net = NeuralNetwork(config)
    net.train(data)  # not implemented

    x_arr = numpy.linspace(-1.0, 1.0, 20)
    line_res = []
    for x in x_arr:
        y = net.process([x])[0]
        line_res.append([x, y])
    log.add_entry('Network was successfully trained.')
    graph.set_line(line_res)


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

    controls.set_load_button_callback(
        lambda: __load_points(controls, graph, log))

    controls.set_launch_button_callback(
        lambda: __launch(controls, graph, log))

    root.mainloop()


if __name__ == '__main__':
    main()
