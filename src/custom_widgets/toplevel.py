"""
MIT License

Copyright (c) 2024 David Southwood

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import tkinter as tk


class Toplevel(tk.Toplevel):
    """
    Custom Toplevel widget that enhances the standard tkinter Toplevel by adding
    functionality for modal behavior and tracking the widget that initiated its creation.

    This class makes it easier to create dialog-like windows that can either operate
    independently or block input to their parent windows until they are closed,
    depending on the modal parameter. Additionally, it keeps a reference to the widget
    or component that called it, which can be useful for back-referencing or performing
    actions related to the caller.

    Attributes:
        called_from (tk.Widget): The widget or component that initiated the creation
                                 of this Toplevel window. This can be any tkinter widget
                                 including but not limited to Frames, Buttons, or other Toplevels.
        modal (bool): Determines whether the Toplevel window should behave as a modal dialog.
                      If True, it will block input to the parent window until it is closed.

    Parameters:
        parent (tk.Widget): The parent widget of this Toplevel window. This is typically
                            an instance of tk.Tk or another Toplevel widget.
        called_from (tk.Widget, optional): The widget or component that is responsible for
                                           creating this Toplevel window. Defaults to None.
        modal (bool, optional): A flag indicating whether the window should act as a modal
                                dialog, blocking input to other windows until dismissed.
                                Defaults to False.

    Example:
        Creating a non-modal custom Toplevel window:

        >>> root = tk.Tk()
        >>> custom_top = Toplevel(root, modal=False)
        >>> custom_top.mainloop()

        Creating a modal custom Toplevel window:

        >>> root = tk.Tk()
        >>> custom_top = Toplevel(root, modal=True)
        >>> custom_top.mainloop()

    Note:
        When 'modal' is set to True, the Toplevel window will call 'transient' to associate
        itself with the parent window and 'grab_set' to direct all input to itself, effectively
        blocking interaction with the parent window until it is closed.
    """
    def __init__(self, parent, called_from=None, modal=False, **kwargs):
        """
        Initializes a new instance of the custom Toplevel widget.

        Parameters:
            parent: The parent widget for this Toplevel window. Typically, this would
                    be an instance of Tk or another Toplevel window.
            called_from: Optional. A reference to the widget or component that is
                         creating this Toplevel window. Default is None.
            modal: Optional. A boolean flag that specifies whether the window should
                   be modal. Default is False.
            **kwargs: Additional keyword arguments that are passed to the tkinter
                      Toplevel initializer. This can include parameters to customize
                      the appearance and behavior of the window, such as title, size,
                      or background color.

        Upon creation, if the `modal` flag is set to True, the window will be set as
        transient for the parent window, and input focus will be grabbed until the
        window is closed, effectively blocking interaction with other windows of the
        application.
        """
        super().__init__(parent, **kwargs)
        self.called_from = called_from
        self.modal = modal

        if self.modal:
            self.transient(parent)
            self.grab_set()
            self.wait_window(self)
