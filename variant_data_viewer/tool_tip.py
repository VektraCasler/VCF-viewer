# variant_data_viewer/tooltip.py
""" Adds tooltips to the application for ease of use. """

# IMPORTS ------------------------------------------------

import tkinter as tk
from tkinter import Widget

# CLASSES ------------------------------------------------

class ToolTip(object):

    def __init__(self, widget) -> None:
        """Initialize Tooltip class."""

        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

        return None

    def showtip(self, text) -> None:
        """Display text in tooltip window."""

        self.text = text
        if self.tipwindow or not self.text:
            return
        
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27

        self.tipwindow = tw = tk.Toplevel(self.widget)

        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))

        label = tk.Label(
            tw,
            text=self.text,
            justify=tk.LEFT,
            background="#ffffe0",
            relief=tk.SOLID,
            borderwidth=1,
            font=("tahoma", "8", "normal"),
        )
        label.pack(ipadx=1)

        return None

    def hidetip(self) -> None:
        """Disappears the tooltip."""

        tw = self.tipwindow
        self.tipwindow = None

        if tw:
            tw.destroy()
        
        return None


# FUNCTIONS -------------------------------------------------------------------

def CreateToolTip(widget: Widget, text) -> None:
    """Creates a floating tooltip object and binds tkinter mouse movements."""
    toolTip = ToolTip(widget)

    def enter(event):
        toolTip.showtip(text)

    def leave(event):
        toolTip.hidetip()

    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

    return None

# MAIN LOOP -------------------------------------------------------------------

def main() -> None:
    """Testing function for module."""

    pass

    return None

if __name__ == "__main__":
    main()
