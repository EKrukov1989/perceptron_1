"""Module for LogWindow-class."""

import enum
import globals
import tkinter as tk
import tkinter.font as tkfont


class EntryType(enum.Enum):
    """This enum defines type of entries in log."""

    INFO = enum.auto()
    WARNING = enum.auto()
    ERROR = enum.auto()


class LogWindow():
    """This class incapsulates logic for work with log.

    It creates text area and scrollbars,
    provides methods for work with content
    """

    __text_widget = None

    def __init__(self, parent_frame):
        """Create text area and scrollbars."""
        logs_frame = tk.Frame(parent_frame)
        logs_frame.place(anchor='nw', relx=0.5, relwidth=0.5, relheight=1.0)
        logs_frame_inner = tk.Frame(logs_frame)
        logs_frame_inner.pack(expand=True, fill='both',
                              padx=(globals.FRAME_PAD, 2*globals.FRAME_PAD),
                              pady=(2*globals.FRAME_PAD, 2*globals.FRAME_PAD))
        logs_frame['bg'] = globals.BG_COLOR
        logs_frame_inner['bg'] = globals.BG_COLOR

        self.__text_widget = tk.Text(logs_frame_inner, wrap=tk.NONE)
        self.__text_widget['font'] = tkfont.Font(family='Consolas', size=12)
        self.__text_widget.config(state=tk.DISABLED)
        self.__text_widget.grid(row=0, column=0, sticky='NSEW')

        yscroll = tk.Scrollbar(logs_frame_inner)
        yscroll.grid(row=0, column=1, sticky='NS')
        xscroll = tk.Scrollbar(logs_frame_inner, orient=tk.HORIZONTAL)
        xscroll.grid(row=1, column=0, sticky='WE')

        self.__text_widget.config(yscrollcommand=yscroll.set)
        yscroll.config(command=self.__text_widget.yview)
        self.__text_widget.config(xscrollcommand=xscroll.set)
        xscroll.config(command=self.__text_widget.xview)

        logs_frame_inner.columnconfigure(0, weight=1)
        logs_frame_inner.rowconfigure(0, weight=1)
        logs_frame_inner.columnconfigure(1, weight=0)
        logs_frame_inner.rowconfigure(1, weight=0)

        self.__text_widget.tag_config('ERROR', foreground="red")

    def add_entry(self, entry, entry_type=EntryType.INFO):
        """Add entry(text) in the end of log.

        Log window will be automatically scrolled down, if required
        """
        assert isinstance(EntryType.INFO, type(entry_type))
        tags = []
        if entry_type is EntryType.ERROR:
            tags.append('ERROR')

        self.__text_widget.config(state=tk.NORMAL)
        self.__text_widget.insert(tk.END, entry + '\n', tags)
        self.__text_widget.config(state=tk.DISABLED)
        self.__text_widget.yview_moveto(1.0)

    def log_err(self, entry):
        """Just for brewity."""
        self.add_entry(entry, EntryType.ERROR)

    def set_content(self, content):
        """Set certain content(text) in the log window.

        Previous content will be removed
        """
        self.__text_widget.config(state=tk.NORMAL)
        self.__text_widget.delete('0.1', tk.END)
        self.__text_widget.config(state=tk.DISABLED)
        self.add_entry(content, EntryType.INFO)
