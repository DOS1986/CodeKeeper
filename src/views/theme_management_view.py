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
from tkinter import ttk, messagebox, PhotoImage, colorchooser, font
from tkinter.colorchooser import askcolor
import re
from src.custom_widgets.font_selector_dialog import FontSelectorDialog
from src.custom_widgets.toplevel import Toplevel
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


class ThemeView:
    """
    summary
    """
    def __init__(self, master, controller_callbacks):
        """
        summary
        """
        logger.info("Initializing ThemeView")
        self.callbacks = controller_callbacks
        self.master = master
        self.frame = Toplevel(master, modal=False, called_from=self)
        self.frame.title("Theme Management")
        self.frame.geometry("1280x800")
        self.theme_data_widgets = {}
        self.create_widgets()

        self.frame.grab_set()

        # This line makes the script wait here until the modal window is closed
        master.wait_window(self.frame)

    def create_widgets(self):
        """
        summary
        """
        self.layout()

    def layout(self):
        """
        summary
        """
        self.frame.grid_columnconfigure(1, weight=1)  # Makes the details frame expandable
        self.frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion

        # Theme list box configuration
        self.theme_listbox = tk.Listbox(self.frame, width=20)
        self.theme_listbox.bind('<<ListboxSelect>>', lambda e: self.on_theme_selected())
        self.theme_listbox.grid(row=0, column=0, sticky="ns", padx=10, pady=5)

        # Details frame configuration
        self.details_frame = ttk.Frame(self.frame)
        self.details_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)
        self.details_frame.grid_columnconfigure(0, weight=1)  # Allow content in details_frame to expand
        self.details_frame.grid_rowconfigure(0, weight=1)  # Allow vertical expansion within details_frame

        # Notebook configuration
        self.notebook = ttk.Notebook(self.details_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        save_button = ttk.Button(self.frame, text="Save", command=self.save_theme)
        save_button.grid(row=1, column=0, sticky="ew", padx=10, pady=5)

    def list_themes(self, themes):
        """
        summary
        """
        self.theme_listbox.delete(0, tk.END)
        for theme in themes:
            self.theme_listbox.insert(tk.END, theme)

    def display_theme_data(self, theme_data):
        """Displays theme data with enhanced UI for editing, using notebook tabs for categories."""
        # Assuming self.notebook is already defined in the class
        for tab in self.notebook.tabs():
            self.notebook.forget(tab)
        self.theme_data_widgets.clear()  # Clear existing widgets

        for category, settings in theme_data.items():
            tab_frame = ttk.Frame(self.notebook)
            tab_frame.grid_rowconfigure(0, weight=0)
            tab_frame.grid_rowconfigure(1, weight=0)
            tab_frame.grid_rowconfigure(2, weight=0)
            tab_frame.grid_rowconfigure(3, weight=0)
            tab_frame.grid_rowconfigure(4, weight=0)
            tab_frame.grid_rowconfigure(5, weight=0)
            tab_frame.grid_rowconfigure(6, weight=0)
            tab_frame.grid_rowconfigure(7, weight=0)
            tab_frame.grid_columnconfigure(0, weight=0)
            tab_frame.grid_columnconfigure(1, weight=0)
            tab_frame.grid_columnconfigure(2, weight=0)
            tab_frame.grid_columnconfigure(3, weight=0)
            tab_frame.grid_columnconfigure(4, weight=0)
            tab_frame.grid_columnconfigure(5, weight=0)
            tab_frame.grid_columnconfigure(6, weight=0)
            tab_frame.grid_columnconfigure(7, weight=0)
            self.notebook.add(tab_frame, text=category.capitalize())

            if category == "ttkStyles":
                # Special handling for ttkStyles to create nested tabs
                self.display_ttk_styles_settings(tab_frame, settings)
            elif category == "colors":
                self.display_colors_in_notebook(tab_frame, settings)
            else:
                self.display_category_settings(tab_frame, settings)

    def display_ttk_styles_settings(self, parent_frame, ttk_styles):
        """Handles the display of ttkStyles settings, including nested 'map' settings."""
        ttk_styles_notebook = ttk.Notebook(parent_frame)
        ttk_styles_notebook.grid(row=0, column=0, sticky="nsew", padx=5)

        for widget_style, style_details in ttk_styles.items():
            style_tab_frame = ttk.Frame(ttk_styles_notebook)
            ttk_styles_notebook.add(style_tab_frame, text=widget_style)

            # Display 'configure' settings directly in the tab
            if "configure" in style_details:
                configure_frame = ttk.LabelFrame(style_tab_frame, text="Configure")
                configure_frame.grid(row=0, column=0,  columnspan=2, sticky="nsew", padx=5)

                self.display_category_settings(configure_frame, style_details["configure"])

            # Handle 'map' settings separately due to their nested nature
            if "map" in style_details:
                self.display_map_settings(style_tab_frame, style_details["map"])

    def display_colors_in_notebook(self, tab_frame, colors_settings):
        """Displays the 'Colors' category settings in a nested notebook for each subcategory."""
        colors_notebook = ttk.Notebook(tab_frame)
        colors_notebook.grid(row=0, column=4,rowspan=4, sticky="ew", padx=10, pady=5)
        row = 0
        for color_category, color_settings in colors_settings.items():
            if isinstance(color_settings, dict):  # For nested settings like 'button', 'treeview', etc.
                color_tab_frame = ttk.Frame(colors_notebook)
                color_tab_frame.grid_rowconfigure(0, weight=0)
                color_tab_frame.grid_rowconfigure(1, weight=0)
                color_tab_frame.grid_rowconfigure(2, weight=0)
                color_tab_frame.grid_rowconfigure(3, weight=0)
                color_tab_frame.grid_rowconfigure(4, weight=0)
                color_tab_frame.grid_rowconfigure(5, weight=0)
                color_tab_frame.grid_rowconfigure(6, weight=0)
                color_tab_frame.grid_rowconfigure(7, weight=0)
                color_tab_frame.grid_columnconfigure(0, weight=0)
                color_tab_frame.grid_columnconfigure(1, weight=0)
                color_tab_frame.grid_columnconfigure(2, weight=0)
                color_tab_frame.grid_columnconfigure(3, weight=0)
                color_tab_frame.grid_columnconfigure(4, weight=0)
                color_tab_frame.grid_columnconfigure(5, weight=0)
                color_tab_frame.grid_columnconfigure(6, weight=0)
                color_tab_frame.grid_columnconfigure(7, weight=0)
                colors_notebook.add(color_tab_frame, text=color_category.capitalize())
                self.display_subcategory_settings(color_tab_frame, color_settings)
            else:
                # Direct color settings, not expected but handled for completeness
                self.create_setting_widget(tab_frame, color_category, color_settings, row)
            row += 1

    def display_category_settings(self, frame, settings):
        """Displays settings for a given category, with handling for nested dictionaries."""
        row = 0
        for key, value in settings.items():
            if isinstance(value, dict):
                # This could be a nested dictionary like in ttkStyles
                sub_frame = ttk.LabelFrame(frame, text=key.capitalize())
                sub_frame.grid(row=row, column=5, sticky="nsew", padx=10, pady=5)
                self.display_category_settings(sub_frame, value)
            else:
                # Display simple settings directly
                self.create_setting_widget(frame, key, value, row)
            row += 1

    def create_setting_widget(self, frame, key, value, row):
        """Creates a setting widget for a given theme setting, with special handling for color values."""
        label = ttk.Label(frame, text=f"{key}:")
        label.grid(row=row, column=0, sticky="w", padx=(10, 2), pady=2)

        entry = ttk.Entry(frame, width=25)
        entry.insert(0, str(value))
        entry.grid(row=row, column=1, sticky="w", padx=5, pady=2)

        if "color" in key.lower() or re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(value)):
            entry.configure(state='readonly')  # Optionally make entry read-only
            color_button = ttk.Button(frame, text="Choose Color", width=15, command=lambda: self.choose_color(key, value))
            color_button.grid(row=row, column=2, sticky="w", padx=5, pady=2)
        elif "font" in key.lower():
            entry.configure(state='readonly')  # Optionally make entry read-only
            font_button = ttk.Button(frame, text="Choose Font", width=15, command=lambda: self.choose_font(key, str(value)))
            font_button.grid(row=row, column=2, sticky="w", padx=5, pady=2)

        # Store the widget for later reference
        self.theme_data_widgets[key] = entry

    def display_subcategory_settings(self, frame, settings):
        """Displays settings for a given subcategory within a frame, especially for nested dictionaries."""
        row = 0
        for key, value in settings.items():
            self.create_setting_widget(frame, key, value, row)
            row += 1

    def display_map_settings(self, parent_frame, map_settings):
        """Displays detailed settings for 'map', considering its nested structure."""
        s = ttk.Style()
        map_frame = ttk.LabelFrame(parent_frame, text="Map")
        map_frame.grid(row=0, column=5, sticky="nsew", padx=5)
        map_frame.columnconfigure(0, weight=1)
        map_frame.rowconfigure(0, weight=1)
        row = 0
        for setting, states in map_settings.items():
            setting_frame = ttk.LabelFrame(map_frame, text=setting.capitalize())
            setting_frame.grid(row=row, column=1, sticky="e", padx=5)
            row += 1
            # Display each state and its value within the setting
            for state_dict in states:
                for state, value in state_dict.items():
                    self.create_map_setting_widget(setting_frame, state, value)

    def create_map_setting_widget(self, frame, state, value):
        """Creates widgets for each state in a 'map' setting."""
        state_label_text = f"{state}:"
        state_label = ttk.Label(frame, text=state_label_text)
        state_label.grid(row=0, column=0, sticky="e", padx=5)

        entry = ttk.Entry(frame, width=25)
        entry.insert(0, str(value))
        entry.grid(row=0, column=1, sticky="ew", padx=5, pady=2)
        frame.grid_columnconfigure(1, weight=1)

        if "color" in state.lower() or re.match(r'^#(?:[0-9a-fA-F]{3}){1,2}$', str(value)):
            entry.configure(state='readonly')  # Optionally make entry read-only
            color_button = ttk.Button(frame, text="Choose Color", command=lambda: self.choose_color(state, value))
            color_button.grid(row=0, column=2, sticky="w", padx=5, pady=2)
        elif "font" in state.lower():
            entry.configure(state='readonly')  # Optionally make entry read-only
            font_button = ttk.Button(frame, text="Choose Font", command=lambda: self.choose_font(state, str(value)))
            font_button.grid(row=0, column=2, sticky="w", padx=5, pady=2)

        self.theme_data_widgets[state] = entry

    def choose_color(self, key, current_color):
        """Opens a color picker dialog and updates the corresponding entry widget."""
        # Open the color chooser dialog and get the chosen color
        chosen_color = colorchooser.askcolor(title="Choose color", initialcolor=current_color)[1]
        if chosen_color:
            # Update the corresponding entry widget with the new color value
            entry_widget = self.theme_data_widgets[key]
            entry_widget.configure(state='normal')  # Temporarily make the widget writable to update its value
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, chosen_color)
            entry_widget.configure(state='readonly')  # Make the widget read-only again

    def choose_font(self, key, current_font):
        """ Opens a font picker dialog and updates the corresponding entry widget."""
        dialog = FontSelectorDialog(self.frame, "Choose Font", current_font)
        if dialog.result:
            # Update the corresponding entry widget with the new color value
            entry_widget = self.theme_data_widgets[key]
            entry_widget.configure(state='normal')  # Temporarily make the widget writable to update its value
            entry_widget.delete(0, 'end')
            entry_widget.insert(0, dialog.result)
            entry_widget.configure(state='readonly')  # Make the widget read-only again

    def on_theme_selected(self):
        """
        summary
        """
        selection = self.theme_listbox.curselection()
        if selection:
            theme_name = self.theme_listbox.get(selection[0])
            self.callbacks['theme_selected'](theme_name)

    def save_theme(self):
        """
        summary
        """
        theme_data = {key: widget.get() for key, widget in self.theme_data_widgets.items()}
        self.callbacks['save_theme'](theme_data)

    def show_message(self, message, success=True):
        """
        Summary
        """
        if success:
            messagebox.showinfo("Success", message, parent=self.frame)
        else:
            messagebox.showerror("Error", message, parent=self.frame)

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
