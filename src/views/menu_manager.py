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


class MenuManager(tk.Menu):
    """MainMenu Class builds a menu for the primary window.

    :param tk: Wrapper functions for Tcl/Tk.
    :type tk: Menu
    """

    def __init__(self, parent, callbacks, **kwargs):
        """THe constructor to initialize the menu.

        :param parent: _description_
        :type parent: _type_
        :param callbacks: _description_
        :type callbacks: _type_
        """
        super().__init__(parent, **kwargs)
        self.callbacks = callbacks

        file_menu = tk.Menu(self, tearoff=False)
        file_menu.add_command(label="New Snippet", command=self.new_snippet, accelerator="Ctrl+N")
        file_menu.add_command(label="Import Snippets")
        file_menu.add_command(label="Export Snippets")
        file_menu.add_separator()
        # add Exit menu item
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit, accelerator="Ctrl+Q")
        self.add_cascade(label="File", underline=0, menu=file_menu)
        # create the Edit menu
        edit_menu = tk.Menu(self, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.open_projects_tab)
        edit_menu.add_command(label="Redo", command=self.open_footprints_tab)
        edit_menu.add_command(label="Cut", command=self.open_manufacturers_tab)
        edit_menu.add_command(label="Copy", command=self.open_storage_locations_tab)
        edit_menu.add_command(label="Past", command=self.open_distributors_tab)
        self.add_cascade(label="Edit", menu=edit_menu)
        # create the View menu
        view_menu = tk.Menu(self, tearoff=0)
        view_menu.add_command(label="Theme Settings")
        view_menu.add_command(label="Language Filters")
        view_menu.add_command(label="Category Filters")
        self.add_cascade(label="View", menu=view_menu)
        # create the Tools menu
        tools_menu = tk.Menu(self, tearoff=0)
        tools_menu.add_command(label="Manage Languages", command=self.about)
        tools_menu.add_command(label="Manage Categories", command=self.about)
        tools_menu.add_command(label="Configuration Settings", command=self.about)
        self.add_cascade(label="Tools", menu=tools_menu)
        # create the Help menu
        help_menu = tk.Menu(self, tearoff=0)
        help_menu.add_command(label="User Guide", command=self.about)
        help_menu.add_command(label="FAQs", command=self.about)
        help_menu.add_command(label="Report Issue", command=self.about)
        help_menu.add_command(label="Suggest Feature", command=self.about)
        help_menu.add_command(label="About", command=self.about)
        self.add_cascade(label="Help", menu=help_menu)

    def new_snippet(self):
        self.callbacks["new_snippet"]()

    def quit(self):
        self.callbacks["file_quit"]()

    def preferences(self):
        self.callbacks["settings_preferences"]()

    def open_projects_tab(self):
        self.callbacks["edit--open_projects_tab"]()

    def open_footprints_tab(self):
        self.callbacks["edit--open_footprints_tab"]()

    def open_manufacturers_tab(self):
        self.callbacks["edit--open_manufacturers_tab"]()

    def open_storage_locations_tab(self):
        self.callbacks["edit--open_storage_locations_tab"]()

    def open_distributors_tab(self):
        self.callbacks["edit--open_distributors_tab"]()

    def open_users_tab(self):
        self.callbacks["edit--open_users_tab"]()

    def open_part_measurement_units_tab(self):
        self.callbacks["edit--open_part_measurement_units_tab"]()

    def open_units_tab(self):
        self.callbacks["edit--open_units_tab"]()

    def about(self):
        self.callbacks["help--about"]()
