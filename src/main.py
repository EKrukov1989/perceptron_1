"""Main module for perceptron_1.

This module consists all logic of top level
"""

import tkinter as tk
from graphwindow import GraphWindow
from logwindow import LogWindow

FRAME_HALF_PAD = 10
BACKGROUND_COLOR = '#666666'


def attach_graph_frame(root):
    """Add canvas for representation of graphic."""
    graph_frame = tk.Frame(root)
    graph_frame['bg'] = BACKGROUND_COLOR
    graph_frame.place(anchor='nw', relwidth=0.5, relheight=0.5)
    graph_frame_inner = tk.Frame(graph_frame)
    graph_frame_inner.pack(expand=True, fill='both',
                           padx=(2*FRAME_HALF_PAD, FRAME_HALF_PAD),
                           pady=(2*FRAME_HALF_PAD, FRAME_HALF_PAD))
    return GraphWindow(graph_frame_inner)


def attach_controls_frame(root):
    """Add controls."""
    controls_frame = tk.Frame(root)
    controls_frame['bg'] = BACKGROUND_COLOR
    controls_frame.place(anchor='nw', rely=0.5, relwidth=0.5, relheight=0.5)
    controls_frame_inner = tk.Frame(controls_frame)
    controls_frame_inner['bg'] = BACKGROUND_COLOR
    controls_frame_inner.pack(expand=True, fill='both',
                              padx=(2*FRAME_HALF_PAD, FRAME_HALF_PAD),
                              pady=(FRAME_HALF_PAD, 2*FRAME_HALF_PAD))

    launchButton = tk.Button(controls_frame_inner, text="Launch", width=12)
    clearButton = tk.Button(controls_frame_inner, text="Clear", width=12)
    launchButton.grid(row=0, column=0, padx=(0, 10))
    clearButton.grid(row=0, column=1)


def attach_logs_frame(root):
    """Add text area for logs."""
    logs_frame = tk.Frame(root)
    logs_frame['bg'] = BACKGROUND_COLOR
    logs_frame.place(anchor='nw', relx=0.5, relwidth=0.5, relheight=1.0)
    logs_frame_inner = tk.Frame(logs_frame)
    logs_frame_inner.pack(expand=True, fill='both',
                          padx=(FRAME_HALF_PAD, 2*FRAME_HALF_PAD),
                          pady=(2*FRAME_HALF_PAD, 2*FRAME_HALF_PAD))
    return LogWindow(logs_frame_inner)


def main():
    """Start application."""
    root = tk.Tk()

    root.wm_iconbitmap('src/images/window.ico')
    root.minsize(800, 600)
    root.state('zoomed')
    root.wm_title('perceptron_1')

    graph_window = attach_graph_frame(root)
    points = [[-0.5, -0.5], [0.5, 0.5]]
    line = [[-0.4, -0.4], [0.4, 0.4]]
    graph_window.set_points(points)
    graph_window.set_line(line)

    log_window = attach_logs_frame(root)
    log_window.add_entry('Area for log')

    attach_controls_frame(root)

    root.mainloop()


if __name__ == '__main__':
    main()
