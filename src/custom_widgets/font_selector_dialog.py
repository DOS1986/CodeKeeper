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
from tkinter import ttk, font
from tkinter.simpledialog import Dialog
import ast


class FontSelectorDialog(Dialog):
    """
    Summary
    """
    def __init__(self, parent, title, initial_font=None):
        """
        Summary
        """
        super().__init__(parent, title)
        self.transient(parent)
        if title:
            self.title(title)

        self.parent = parent
        self.result = None

        # If initial_font is a string, convert it back to a list
        if isinstance(initial_font, str):
            try:
                # Safely evaluate the string to a Python literal
                self.initial_font = ast.literal_eval(initial_font)
                # Ensure the evaluated result is a list with expected length
                if not isinstance(self.initial_font, list) or len(self.initial_font) < 2:
                    raise ValueError("Initial font does not have the expected format.")
            except (ValueError, SyntaxError):
                self.initial_font = ["Arial", 10, "normal"]  # Default value if parsing fails
        else:
            self.initial_font = initial_font or ["Arial", 10, "normal"]

        self.body(self.body)

        self.grab_set()
        self.wait_window(self)

    def body(self, body):
        """
        Create dialog body. Set up labels and inputs for font selection.
        """
        ttk.Label(self, text="Font Family:").grid(row=0, sticky=tk.W)
        ttk.Label(self, text="Font Size:").grid(row=1, sticky=tk.W)
        ttk.Label(self, text="Font Style:").grid(row=2, sticky=tk.W)

        # Convert initial font list to suitable format for entry and comboboxes
        self.font_family_var = tk.StringVar(value=self.initial_font[0])
        self.font_size_var = tk.StringVar(value=str(self.initial_font[1]))
        self.font_style_var = tk.StringVar(value=self.initial_font[2])

        # Use actual font families and limited styles for demonstration
        font_families = list(tk.font.families())
        font_styles = ["normal", "bold", "italic", "bold italic"]

        self.font_family_entry = ttk.Combobox(self.parent, textvariable=self.font_family_var, values=font_families, state="readonly")
        self.font_size_entry = ttk.Entry(self.parent, textvariable=self.font_size_var)
        self.font_style_entry = ttk.Combobox(self.parent, textvariable=self.font_style_var, values=font_styles, state="readonly")

        self.font_family_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.font_size_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.font_style_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        return self.font_family_entry  # initial focus

    def apply(self):
        """
        Process the dialog result.
        """
        try:
            font_size = int(self.font_size_var.get())  # Ensure the size is an integer
        except ValueError:
            font_size = 10  # Default or previous value if conversion fails

        selected_font = [
            self.font_family_var.get(),
            font_size,
            self.font_style_var.get()
        ]
        self.result = selected_font
