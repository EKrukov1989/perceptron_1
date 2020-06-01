"""Main module for perceptron_1.

This module consists all logic of top level
"""

import tkinter as ttk
import tkinter.font as ttkfont

FRAME_HALF_PAD = 10
BACKGROUND_COLOR = '#666666'


def attach_graph_frame(root):
    """Add canvas for representation of graphic."""
    graph_frame = ttk.Frame(root)
    graph_frame['bg'] = BACKGROUND_COLOR
    graph_frame.place(anchor='nw', relwidth=0.5, relheight=0.5)
    graph_frame_inner = ttk.Frame(graph_frame)
    graph_frame_inner.pack(expand=True, fill='both',
                           padx=(2*FRAME_HALF_PAD, FRAME_HALF_PAD),
                           pady=(2*FRAME_HALF_PAD, FRAME_HALF_PAD))
    graph_canvas = ttk.Canvas(graph_frame_inner)
    graph_canvas['bg'] = 'white'
    graph_canvas['highlightthickness'] = 0
    graph_canvas.place(anchor='nw', relwidth=1.0, relheight=1.0)

    def redraw(e):
        graph_canvas.delete('axis')
        graph_canvas.create_line(0, 0.5*e.height, e.width, 0.5*e.height,
                                 tags='axis', fill='blue')
        graph_canvas.create_line(0.5*e.width, 0, 0.5*e.width, e.height,
                                 tags='axis', fill='red')
    graph_canvas.bind('<Configure>', redraw)


def attach_controls_frame(root):
    """Add controls."""
    controls_frame = ttk.Frame(root)
    controls_frame['bg'] = BACKGROUND_COLOR
    controls_frame.place(anchor='nw', rely=0.5, relwidth=0.5, relheight=0.5)
    controls_frame_inner = ttk.Frame(controls_frame)
    controls_frame_inner['bg'] = BACKGROUND_COLOR
    controls_frame_inner.pack(expand=True, fill='both',
                              padx=(2*FRAME_HALF_PAD, FRAME_HALF_PAD),
                              pady=(FRAME_HALF_PAD, 2*FRAME_HALF_PAD))

    launchButton = ttk.Button(controls_frame_inner, text="Launch", width=12)
    clearButton = ttk.Button(controls_frame_inner, text="Clear", width=12)
    launchButton.grid(row=0, column=0, padx=(0, 10))
    clearButton.grid(row=0, column=1)


def attach_logs_frame(root):
    """Add text area for logs."""
    logs_frame = ttk.Frame(root)
    logs_frame['bg'] = BACKGROUND_COLOR
    logs_frame.place(anchor='nw', relx=0.5, relwidth=0.5, relheight=1.0)
    logs_frame_inner = ttk.Frame(logs_frame)
    logs_frame_inner.pack(expand=True, fill='both',
                          padx=(FRAME_HALF_PAD, 2*FRAME_HALF_PAD),
                          pady=(2*FRAME_HALF_PAD, 2*FRAME_HALF_PAD))

    logs_area = ttk.Text(logs_frame_inner, wrap=ttk.NONE)
    logs_area.insert('1.0', 'Area for logs')
    logs_area['font'] = ttkfont.Font(family='Consolas', size=12)
    logs_area.config(state=ttk.DISABLED)
    logs_area.grid(row=0, column=0, sticky='NSEW')

    yscroll = ttk.Scrollbar(logs_frame_inner)
    yscroll.grid(row=0, column=1, sticky='NS')
    xscroll = ttk.Scrollbar(logs_frame_inner, orient=ttk.HORIZONTAL)
    xscroll.grid(row=1, column=0, sticky='WE')

    logs_area.config(yscrollcommand=yscroll.set)
    yscroll.config(command=logs_area.yview)
    logs_area.config(xscrollcommand=xscroll.set)
    xscroll.config(command=logs_area.xview)

    logs_frame_inner.columnconfigure(0, weight=1)
    logs_frame_inner.rowconfigure(0, weight=1)
    logs_frame_inner.columnconfigure(1, weight=0)
    logs_frame_inner.rowconfigure(1, weight=0)


def main():
    """Start application."""
    root = ttk.Tk()

    root.wm_iconbitmap('src/images/window.ico')
    root.minsize(800, 600)
    root.state('zoomed')
    root.wm_title('perceptron_1')

    attach_graph_frame(root)
    attach_logs_frame(root)
    attach_controls_frame(root)

    root.mainloop()


if __name__ == '__main__':
    main()
