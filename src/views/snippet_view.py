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
from tkinter import ttk, messagebox, simpledialog

from src.custom_widgets.toplevel import Toplevel
from src.utils.configuration_manager import ConfigurationManager


class SnippetView:
    """
    Summary
    """

    def __init__(self, master, controller_callbacks):
        """
        Summary
        """
        self.callbacks = controller_callbacks
        self.master = master
        self.frame = Toplevel(master, modal=False, called_from=self)
        self.languages = self.load_languages()
        self.create_widgets()

        self.frame.grab_set()

        # This line makes the script wait here until the modal window is closed
        master.wait_window(self.frame)

    def load_languages(self):
        """
        Summary
        """
        # Instantiate ConfigurationManager with the specific config name
        config_manager = ConfigurationManager("application_config")

        # Get languages configuration
        languages_config = config_manager.get_configuration("languages", {})

        # Extract built-in and custom languages
        builtin_languages = [lang["language"] for lang in languages_config.get("builtin", [])]
        custom_languages = [lang["language"] for lang in languages_config.get("custom", [])]

        # Combine both lists
        all_languages = builtin_languages + custom_languages

        return all_languages

    def create_widgets(self):
        """
        Summary
        """
        self.title_var = tk.StringVar()
        self.language_var = tk.StringVar()
        self.code_text = tk.Text(self.frame, height=15, width=50)

        ttk.Label(self.frame, text="Title:").grid(row=0, column=0, sticky="w")
        ttk.Entry(self.frame, textvariable=self.title_var).grid(row=0, column=1, sticky="ew")

        self.language_dropdown = ttk.Combobox(self.frame, textvariable=self.language_var, values=self.languages, state="readonly")
        self.language_dropdown.grid(row=1, column=1, sticky="ew")
        ttk.Label(self.frame, text="Language:").grid(row=1, column=0, sticky="w")

        ttk.Label(self.frame, text="Code:").grid(row=2, column=0, sticky="nw")
        self.code_text.grid(row=2, column=1, sticky="nsew")

        submit_btn = ttk.Button(self.frame, text="Submit", command=self.on_submit_click)
        submit_btn.grid(row=3, column=1, sticky="e")

        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(2, weight=1)

    def on_submit_click(self):
        """
        Summary
        """
        self.data = {
            'title': self.title_var.get(),
            'language': self.language_var.get(),
            'code': self.code_text.get("1.0", "end-1c")
        }
        self.callbacks["submit_snippet"](self.data)

    def show_message(self, message, success=True):
        """
        Summary
        """
        if success:
            messagebox.showinfo("Success", message, parent=self.frame)
        else:
            messagebox.showerror("Error", message, parent=self.frame)

    def clear_form(self):
        """
        Summary
        """
        self.title_var.set("")
        self.language_var.set("")
        self.code_text.delete("1.0", "end")

    def populate_form(self, snippet):
        """
        Populates the form with data for editing. Called if the controller is in 'edit' mode.
        """
        print(snippet)
        self.title_var.set(snippet['title'])
        self.language_var.set(snippet['language'])
        self.code_text.delete('1.0', tk.END)
        self.code_text.insert(tk.END, snippet['code'])

    def show(self):
        """
        summary
        """
        # This method makes the window visible. Depending on your UI framework,
        # the actual implementation might differ.
        if self.frame.winfo_exists():
            self.frame.deiconify()  # Make sure the window is visible
            self.frame.wait_window()

    def close(self):
        """Closes the snippet form window."""
        self.frame.destroy()
