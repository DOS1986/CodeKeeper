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
from tkinter import ttk
from tkinter.ttk import Scrollbar
from src.custom_widgets.toplevel import Toplevel
# from src.utils.configuration_manager import ConfigurationManager


def add_tooltip(widget, text):
    """ summary"""

    def show_tooltip(event):
        """summary"""
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        # Ideally, create a tooltip window (Toplevel) with the 'text'
        print(f"Tooltip: {text}")  # Placeholder print statement

    widget.bind("<Enter>", show_tooltip)
    # Add additional logic to hide tooltip on "<Leave>" if using Toplevel for tooltips


def create_category_ui(parent, category_name, path):
    """
    Creates a UI section or category to group related configuration settings.

    Args:
        parent (tk.Widget): The parent widget.
        category_name (str): The name of the category.
        path (str): The path to the category within the configuration structure.
    """
    frame = ttk.LabelFrame(parent, text=category_name, padding="10 10 10 10")
    frame.pack(fill='x', expand=True, padx=5, pady=5)
    return frame


def create_subsection_ui(parent, subsection_name):
    """
    Creates a UI subsection for nested configuration data.

    Args:
        parent (tk.Widget): The parent widget.
        subsection_name (str): The name of the subsection.

    Returns:
        tk.Widget: The created subsection UI element, ready for adding further elements.
    """
    frame = ttk.Frame(parent, padding="10 10 10 10")
    frame.pack(fill='x', expand=True, padx=5, pady=5)
    label = ttk.Label(frame, text=subsection_name, font=('TkDefaultFont', 10, 'bold'))
    label.pack(side="top", fill='x')
    return frame


def create_list_item_ui(parent, index, path):
    """
    Optionally creates a UI element for a list item in the configuration.

    Args:
        parent (tk.Widget): The parent widget.
        index (int): The index of the item in the list.
        path (str): The path to the item within the configuration structure.
    """
    label = ttk.Label(parent, text=f"Item {index + 1}", font=('TkDefaultFont', 9, 'italic'))
    label.pack(side="top", fill='x', pady=2)
    return label


def create_config_widget(parent, label, value, path):
    """
    Creates UI widgets dynamically based on the configuration data type and its path.

    Args:
        parent (tk.Widget): The parent widget where this config widget will be placed.
        label (str): The label for the configuration setting.
        value: The current value of the configuration setting.
        path (str): The hierarchical path to this setting within the configuration structure.
    """
    frame = ttk.Frame(parent)
    frame.pack(fill='x', padx=5, pady=2)

    lbl = ttk.Label(frame, text=label)
    lbl.pack(side='left')

    # Optional: Tooltip displaying the full path for clarity
    tooltip = f"Path: {path}\nClick for more options."
    add_tooltip(lbl, f"Config key: {label}")

    # Handling different types of values with appropriate UI elements
    if isinstance(value, bool):
        var = tk.BooleanVar(value=value)
        entry = ttk.Checkbutton(frame, variable=var)
    elif isinstance(value, int):
        var = tk.IntVar(value=value)
        entry = ttk.Spinbox(frame, from_=0, to=100, textvariable=var)
    elif isinstance(value, list):  # Example for a dropdown
        var = tk.StringVar(value=value[0])
        entry = ttk.Combobox(frame, values=value, textvariable=var)
    else:  # Default to text entry for other types
        var = tk.StringVar(value=str(value))
        entry = ttk.Entry(frame, textvariable=var)

    entry.pack(side='right', expand=True, fill='x')


def center_window(window):
    """
    Summary
    """
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))


class ConfigurationView:
    """
    summary
    """

    def __init__(self, master, controller_callbacks):
        self.callbacks = controller_callbacks
        self.window = Toplevel(master, modal=False, called_from=self)
        self.window.title("Preferences")
        self.window.geometry("600x400")

        self.application_config = self.callbacks["load_configuration"]("application")
        self.logging_config = self.callbacks["load_configuration"]("logging")
        self.preferences_config = self.callbacks["load_configuration"]("preferences")

        self.setup_search_bar()
        self.create_widgets()
        center_window(self.window)

        self.breadcrumb_var = tk.StringVar()
        self.breadcrumb_var.set("Application")  # Default value

        self.original_treeview_data = []

        # self.show()

        self.window.grab_set()

        # This line makes the script wait here until the modal window is closed
        master.wait_window(self.window)

    def update_breadcrumb(self, path):
        """
        Updates the breadcrumb navigation based on the current path.

        Args:
            path (str): The current navigation path.
        """
        self.breadcrumb_var.set(path)

    def create_widgets(self):
        """
        summary
        """
        # Create frames
        self.navigation_frame = ttk.Frame(self.window, width=200, padding="3")
        self.navigation_frame.pack(side="left", fill="y")

        self.canvas = tk.Canvas(self.window, borderwidth=0)  # self refers to the main preferences view frame/window
        self.content_frame = ttk.Frame(self.canvas, padding="3")
        self.scrollbar = ttk.Scrollbar(self.canvas, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="right", fill="both", expand=True)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw", tags="self.content_frame")

        # self.content_frame.pack(side="right", expand=True, fill="both")

        # Setup TreeView
        self.tree = ttk.Treeview(self.navigation_frame, selectmode='browse')
        self.tree.pack(expand=True, fill="both")

        # Add categories to TreeView
        self.setup_treeview()

        # Bind TreeView selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_selection)

        self.canvas.bind('<Configure>', self.on_canvas_configure)
        self.window.bind('<Configure>', self.on_window_configure)
        self.content_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind('<Configure>', self.frame_width)

        self.canvas.bind("<MouseWheel>", self.on_mousewheel)  # For Windows
        self.canvas.bind("<Button-4>", self.on_linux_scroll_up)  # For Linux scroll up
        self.canvas.bind("<Button-5>", self.on_linux_scroll_down)  # For Linux scroll down

        self.canvas.bind("<Enter>", lambda e: self.canvas.focus_set())

    def on_canvas_configure(self, event):
        """
        summary
        """
        self.update_scrollbar_visibility()

    def on_window_configure(self, event):
        """
        summary
        """
        # Optionally, a slight delay before updating can help with handling rapid resize events.
        self.window.after(100, self.update_scrollbar_visibility)

    def on_mousewheel(self, event):
        """Handles mouse wheel scrolling for Windows and macOS."""
        # Windows uses 'delta' for the amount scrolled
        if event.delta:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # macOS uses a different 'delta'
        else:
            self.canvas.yview_scroll(int(-1 * event.delta), "units")

    def on_linux_scroll_up(self, event):
        """Handles scroll up events for Linux."""
        self.canvas.yview_scroll(-1, "units")

    def on_linux_scroll_down(self, event):
        """Handles scroll down events for Linux."""
        self.canvas.yview_scroll(1, "units")

    def on_frame_configure(self, event=None):
        """Reset the scroll region to encompass the inner frame."""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.update_scrollbar_visibility()
        # Adjust the content frame's width here as well if needed

    def update_scrollbar_visibility(self):
        """
        summary
        """
        canvas_height = self.canvas.winfo_height()
        _, _, _, content_height = self.canvas.bbox("all")

        # If content height is less than or equal to canvas viewport height, hide the scrollbar.
        if content_height <= canvas_height:
            self.scrollbar.pack_forget()
            self.canvas.configure(yscrollcommand="None")
        else:
            self.scrollbar.pack(side="right", fill="y")
            self.canvas.configure(yscrollcommand=self.scrollbar.set)

    def frame_width(self, event):
        """Dynamically adjust the width of the content frame to fit within the canvas."""
        canvas_width = event.width
        # Assuming the scrollbar width is 20 pixels; adjust this based on your theme or dynamically retrieve it
        scrollbar_width = 20
        new_width = canvas_width - scrollbar_width
        self.canvas.itemconfig("self.content_frame", width=new_width)

    def setup_treeview(self):
        """
        summary
        """
        # Reset the data list whenever you're setting up or refreshing the TreeView
        self.original_treeview_data = []

        # Define parent nodes and their configurations in a structured way
        categories = [
            {"id": "Application", "configurations": self.application_config},
            {"id": "Preferences", "configurations": self.preferences_config},
            {"id": "Logging", "configurations": self.logging_config},
        ]

        # Iterate over each category and populate both the TreeView and the data list
        for category in categories:
            parent_id = self.tree.insert("", "end", text=category["id"], open=True)

            # Store information about the parent node
            self.original_treeview_data.append({
                "id": parent_id,
                "text": category["id"],
                "parent": "",
                "type": "category"
            })

            for key in category["configurations"].keys():
                item_id = self.tree.insert(parent_id, 'end', text=key, iid=key, open=True)

                # Store information about each child node
                self.original_treeview_data.append({
                    "id": item_id,
                    "text": key,
                    "parent": parent_id,
                    "type": "item"
                })

    def get_config_data(self, selected_item):
        """
        summary
        """
        # Assuming 'configurations' attribute contains the data
        for config in (self.preferences_config, self.application_config, self.logging_config):
            if selected_item in config:
                return config[selected_item]
        return None

    def on_tree_selection(self, event):
        """
        Handles the selection of an item in the treeview and updates the UI accordingly.
        """
        selected_item = self.tree.selection()[0]  # Assuming single selection

        # Check if the selected item is a root-level node
        if self.is_root_level_node(selected_item):
            # Update the breadcrumb to just show the root item name
            item_text = self.tree.item(selected_item, 'text')
            self.update_breadcrumb(item_text)
            # Clear existing widgets
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            # Skip widget generation for root-level nodes
            return

        # Dynamically construct the breadcrumb path including the root item's name
        root_item_name, breadcrumb_path = self.construct_breadcrumb_path(selected_item)
        # Update the breadcrumb UI using the root item's name as the starting point
        self.update_breadcrumb(f"{root_item_name} > {' > '.join(breadcrumb_path)}")

        # Clear existing widgets
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        # Get the configuration data for the selected item
        config_data = self.get_config_data(selected_item)

        # Populate the details UI with the configuration data
        self.populate_details_ui(self.content_frame, config_data)

    def is_root_level_node(self, item_id):
        """
        Checks if the selected item is a root-level node.

        Args:
            item_id (str): The ID of the selected item in the treeview.

        Returns:
            bool: True if the selected item is a root-level node, False otherwise.
        """
        # Option 1: Check if the item has no parent (root items have '')
        return self.tree.parent(item_id) == ''

        # Option 2: Check against a list of known root-level node names
        # item_text = self.tree.item(item_id, 'text')
        # root_items = ["Application", "Preferences", "Logging"]
        # return item_text in root_items

    def construct_breadcrumb_path(self, item_id):
        """
        Constructs the breadcrumb path for the given item in the treeview, including the root item's name.

        Args:
            item_id (str): The ID of the selected item in the treeview.

        Returns:
            tuple: A tuple where the first element is the root item's name and the second is a list of strings representing
                   the path from the root to the selected item.
        """
        path = []
        current_item = item_id
        root_item_name = ""
        while current_item:  # Trace back to the root
            item_text = self.tree.item(current_item, 'text')
            path.insert(0, item_text)  # Insert at the beginning to build the path backwards
            root_item_name = item_text  # Keep updating until the last iteration
            current_item = self.tree.parent(current_item)  # Move up to the parent
        return root_item_name, path[1:]  # Exclude the root item name from the path list

    def populate_details_ui(self, parent, config_data, path=''):
        """
        Dynamically creates UI elements to display and edit configuration settings.

        Args:
            parent (tk.Widget): The parent widget to contain the generated UI elements.
            config_data (dict | list | any): The configuration data to be displayed. Can be a dictionary,
                a list, or single value items.
            path (str): The hierarchical path to the current configuration setting, used for identifying
                and updating settings.
        """
        if isinstance(config_data, dict):
            for key, value in config_data.items():
                new_path = f"{path}/{key}" if path else key

                # Check if 'value' is a simple type or a dict with metadata
                if isinstance(value, dict) and 'type' in value:
                    # 'value' is a dict with metadata indicating a dynamic field
                    self.create_dynamic_field(self.sub_frame if 'sub_frame' in locals() else parent, key, value,
                                              new_path)
                elif isinstance(value, (dict, list)):
                    # Create a sub-section for nested structures
                    create_category_ui(parent, key, new_path)
                    self.sub_frame = create_subsection_ui(parent, key)
                    self.populate_details_ui(self.sub_frame, value, new_path)
                else:
                    # 'value' is a simple type without explicit metadata
                    create_config_widget(self.sub_frame if 'sub_frame' in locals() else parent, key, value,
                                              new_path)
        elif isinstance(config_data, list):
            for index, item in enumerate(config_data):
                new_path = f"{path}/{index}"
                create_list_item_ui(parent, index, new_path)
                if isinstance(item, (dict, list)):
                    self.sub_frame = create_subsection_ui(parent, f"Item {index}")
                    self.populate_details_ui(self.sub_frame, item, new_path)
                else:
                    create_config_widget(self.sub_frame if 'sub_frame' in locals() else parent, f"Item {index}",
                                              item, new_path)
        else:
            # Single non-dict, non-list item
            create_config_widget(parent, path.split('/')[-1] if path else "Value", config_data, path)

    def create_dynamic_field(self, parent, label, value, path):
        """
        Creates UI widgets dynamically based on the field's metadata, including its type and options.

        Args:
            parent (tk.Widget): The parent widget where this config widget will be placed.
            label (str): The label for the configuration setting.
            value (dict): A dictionary containing the field's type, actual value, and possibly other metadata.
            path (str): The hierarchical path to this setting within the configuration structure.
        """
        frame = ttk.Frame(parent)
        frame.pack(fill='x', padx=5, pady=2)

        lbl = ttk.Label(frame, text=label)
        lbl.pack(side='left', padx=5)

        # Assume 'value' is a dict containing the type and actual value or options
        field_type = value.get("type")
        field_value = value.get("value")
        options = value.get("options", [])

        if field_type == "bool":
            var = tk.BooleanVar(value=field_value)
            entry = ttk.Checkbutton(frame, variable=var)
        elif field_type == "int":
            var = tk.IntVar(value=field_value)
            entry = ttk.Spinbox(frame, from_=0, to=100, textvariable=var, validate="key",
                                validatecommand=(parent.register(self.is_valid_integer), '%P'))
        elif field_type == "list":
            var = tk.StringVar(value=field_value)
            entry = ttk.Combobox(frame, values=options, textvariable=var)
        else:
            var = tk.StringVar(value=str(field_value))
            entry = ttk.Entry(frame, textvariable=var)

        entry.pack(side='right', expand=True, fill='x')

        # Optional: Add a tooltip for the field
        add_tooltip(entry, f"Config key: {label}")

    def is_valid_integer(self, P):
        """Summary"""
        if not P or P.isdigit():
            return True
        self.window.bell()  # Sound bell if not valid
        return False

    def show_context_menu(self, event, path):
        """
        Displays a context menu for a configuration widget with various options.

        Args:
            event: The event object containing information about the click.
            path (str): The path of the configuration setting, used to identify it uniquely.
        """
        menu = tk.Menu(self.content_frame, tearoff=0)
        menu.add_command(label="Reset to Default", command=lambda: self.reset_to_default(path))
        menu.add_command(label="Help", command=lambda: self.show_help_for_path(path))
        # Position the menu at the cursor's location
        menu.tk_popup(event.x_root, event.y_root)

    def reset_to_default(self, path):
        """
        Resets the configuration setting at the given path to its default value.

        Args:
            path (str): The path of the configuration setting to reset.
        """
        # Placeholder for reset logic, which would likely involve looking up
        # the default value from somewhere and updating both the internal state
        # and the UI accordingly.
        pass

    def show_help_for_path(self, path):
        """
        Displays help or documentation related to a specific configuration setting.

        Args:
            path (str): The path of the configuration setting for which to show help.
        """
        # Placeholder for showing help, which could involve opening a dialog
        # with detailed information or documentation about the setting.
        pass

    def setup_search_bar(self):
        """
        summary
        """
        search_frame = ttk.Frame(self.window)
        search_frame.pack(side="top", fill="x", padx=5, pady=5)
        search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=search_var)
        search_entry.pack(side='left', fill='x', expand=True)
        search_button = ttk.Button(search_frame, text='Search', command=lambda: self.filter_treeview(search_var.get()))
        search_button.pack(side='right')

        # Ensure this callback triggers on every change to the search_var
        search_var.trace_add("write", lambda name, index, mode, sv=search_var: self.filter_treeview(sv.get()))

    def filter_treeview(self, search_query):
        """
        Filters the TreeView to only display items matching the search query.
        If the search query is empty, the TreeView is reset to show all items.

        Args:
            search_query (str): The text to search for within the TreeView items.
        """
        # Clear the TreeView
        for item in self.tree.get_children():
            self.tree.delete(item)

        matched_items = []  # List to keep track of items that match the query

        if not search_query.strip():
            # If search query is empty, reset TreeView to show all items
            self.setup_treeview()
        else:
            # Create a temporary dictionary to hold filtered data by categories
            filtered_data_by_category = {}
            for item in self.original_treeview_data:
                if item['type'] == 'item' and search_query.lower() in item['text'].lower():
                    # If the item matches the search query, add it under the appropriate category
                    parent = item['parent']
                    if parent not in filtered_data_by_category:
                        filtered_data_by_category[parent] = [item]
                    else:
                        filtered_data_by_category[parent].append(item)

            # Re-populate TreeView with filtered items, including their parent categories
            for parent_id, items in filtered_data_by_category.items():
                # Find the parent item's text from original data
                parent_text = next((item['text'] for item in self.original_treeview_data if item['id'] == parent_id),
                                   None)
                if parent_text:
                    parent_in_tree = self.tree.insert("", "end", text=parent_text, open=True)
                    for item in items:
                        id = self.tree.insert(parent_in_tree, "end", text=item['text'], iid=item['id'], open=True)
                        matched_items.append(id)

            if matched_items:
                self.tree.selection_set(matched_items[0])  # Select the first match
                self.tree.see(matched_items[0])  # Ensure the selected item is visible
                self.on_tree_selection(None)  # Manually trigger the selection event handler if needed

    def show(self):
        """
        summary
        """
        # This method makes the window visible. Depending on your UI framework,
        # the actual implementation might differ.
        if self.window.winfo_exists():
            self.window.deiconify()  # Make sure the window is visible
            self.window.wait_window()

    def close(self):
        """Closes the snippet form window."""
        self.window.destroy()
