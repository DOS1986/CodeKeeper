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
import json
import os


class NewThemeDialog(Dialog):
    def __init__(self, parent, title, template_path, themes_directory):
        self.template_path = template_path
        self.themes_directory = themes_directory
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Theme Name:").grid(row=0)
        self.theme_name_entry = tk.Entry(master)
        self.theme_name_entry.grid(row=0, column=1)
        return self.theme_name_entry

    def apply(self):
        theme_name = self.theme_name_entry.get()
        if theme_name:
            self.create_new_theme_from_template(theme_name)

    def create_new_theme_from_template(self, theme_name):
        new_theme_path = os.path.join(self.themes_directory, f"{theme_name}.json")
        if os.path.exists(new_theme_path):
            tk.messagebox.showerror("Error", "Theme already exists.")
            return False
        try:
            with open(self.template_path, 'r') as template_file:
                template_data = json.load(template_file)
            with open(new_theme_path, 'w') as new_theme_file:
                json.dump(template_data, new_theme_file, indent=4)
            tk.messagebox.showinfo("Success", "New theme created successfully.")
            return True
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to create theme: {e}")
            return False
