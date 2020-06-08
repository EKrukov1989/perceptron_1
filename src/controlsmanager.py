"""The module for ControlsManager class."""

import globals
import tkinter as tk
import tkinter.font as tkfont


class ControlsManager():
    """Incapsulates all logic for control panel.

    Creates controls and provides access to them
    """

    __data_path_widget = None
    __config_path_widget = None
    __load_button = None
    __launch_button = None

    def __init__(self, parent_frame):
        """Create controls."""
        controls_frame = tk.Frame(parent_frame)
        controls_frame.place(anchor='nw', rely=0.5,
                             relwidth=0.5, relheight=0.5)
        inner_frame = tk.Frame(controls_frame)
        inner_frame.pack(expand=True, fill='both',
                         padx=(2*globals.FRAME_PAD, globals.FRAME_PAD),
                         pady=(globals.FRAME_PAD, 2*globals.FRAME_PAD))
        controls_frame['bg'] = globals.BG_COLOR
        inner_frame['bg'] = globals.BG_COLOR

        data_entry_label = tk.Label(inner_frame, text="Data path:",
                                    bg=globals.BG_COLOR)
        config_entry_label = tk.Label(inner_frame, text="Config path:",
                                      bg=globals.BG_COLOR)

        data_entry = tk.Entry(inner_frame, width=35)
        data_entry['font'] = tkfont.Font(family='Consolas', size=10)
        data_entry.insert(0, globals.DEFAULT_DATA_PATH)

        config_entry = tk.Entry(inner_frame, width=35)
        config_entry['font'] = tkfont.Font(family='Consolas', size=10)
        config_entry.insert(0, globals.DEFAULT_CONFIG_PATH)

        data_entry_label.grid(row=0, column=0, sticky='W',
                              padx=(0, 20), pady=(0, 10))
        data_entry.grid(row=0, column=1, sticky='E', pady=(0, 10))
        config_entry_label.grid(row=1, column=0, sticky='W', pady=(0, 10))
        config_entry.grid(row=1, column=1, sticky='E', pady=(0, 10))

        load_button = tk.Button(inner_frame, text="Load train data", width=15)
        load_button.grid(row=2, column=0, columnspan=2,
                         sticky='W', pady=(0, 10))

        launch_button = tk.Button(inner_frame, text="Launch", width=15)
        launch_button.grid(row=3, column=0, columnspan=2,
                           sticky='W', pady=(0, 10))

        self.__data_path_widget = config_entry
        self.__data_path_widget = data_entry
        self.__load_button = load_button
        self.__launch_button = launch_button

    def get_data_path(self):
        """Return path for data-file."""
        return self.__data_path_widget.get()

    def get_configuration_path(self):
        """Return path for configuration-file."""
        return self.__config_path_widget.get('0.1', tk.END)

    def set_load_button_callback(self, cbk):
        """No."""
        self.__load_button.config(command=cbk)

    def set_launch_button_callback(self, cbk):
        """No."""
        self.__launch_button.config(command=cbk)
