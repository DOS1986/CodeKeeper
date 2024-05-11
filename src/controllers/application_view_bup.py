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
import os
import tkinter
import tkinter as tk
from tkinter import ttk, messagebox, PhotoImage, Toplevel
from PIL import Image, ImageTk
from src.utils.theme import theme_manager
from src.utils.constants import MAIN_WINDOW_SIZE, APPLICATION_NAME, IMAGES_DIR
from src.utils.custom_logger import CustomLogger

# Instantiate the logger
logger = CustomLogger(__name__).logger


def show_warning_message(message):
    """Displays a warning message dialog to the user."""
    messagebox.showwarning("Warning", message)


def show_info_message(message):
    """Displays an informational message dialog to the user."""
    messagebox.showinfo("Info", message)


def show_error_message(message):
    """Displays an error message dialog to the user."""
    messagebox.showerror("Error", message)


def edit_snippet(treeview, item_id, new_name):
    """Edit the name of an existing snippet."""
    treeview.item(item_id, text=new_name)


def add_snippet(self, snippet_data):
    """Add a new snippet under a specified parent."""
    language = snippet_data['language']
    category = snippet_data['category'] if snippet_data['category'] else "No Category"
    snippet_title = snippet_data['title']
    snippet_id = snippet_data['id']  # Assuming each snippet has a unique ID

    # Find or create the language node
    language_node = self.find_or_create_node('', language)

    # Find or create the category node, under the language node
    category_node = self.find_or_create_node(language_node, category)

    # Now, add the snippet under the category node
    self.treeview.insert(category_node, 'end', iid=snippet_id, text=snippet_title, values=...)


def delete_snippet(treeview, item_id):
    """Delete an existing snippet."""
    treeview.delete(item_id)


def find_or_create_node(self, parent, title):
    """
    summary
    """
    # Check if the node exists under the parent
    for child in self.treeview.get_children(parent):
        if self.treeview.item(child, 'text') == title:
            return child  # Node exists, return its ID


class ApplicationView:
    """
    The ApplicationView class represents the graphical user interface of the application,
    handling the layout, presentation, and user interactions.

    It manages the creation, configuration, and interaction of UI widgets, applying themes,
    and invoking controller callbacks based on user actions. It acts within the MVC architectural
    pattern as the View component, interpreting user inputs and presenting the data.

    Attributes:
        callbacks (dict): Mapping of UI actions to controller callback functions.
        root (tk.Tk): The root window of the application's GUI.
    """

    def __init__(self, controller_callbacks):
        """
        Initializes the ApplicationView with necessary callbacks, sets up the main window, and initializes the UI.

        Args:
            controller_callbacks (dict): A dictionary mapping UI actions to controller callback functions.
        """
        self.last_selected_item = None
        self.last_clicked_item = None
        self.general_categories = None
        self.language_specific_categories = None
        self.callbacks = controller_callbacks
        self.root = tk.Tk()
        self.style = ttk.Style(self.root)
        self.them_manager = theme_manager
        self.initialize_main_window()
        self.initialize_ui()

    def initialize_main_window(self):
        """
        Sets up the main window of the application including geometry, title, and application icon.
        It also configures the main window to be the primary visible window while hiding the root window.
        """
        self.top = Toplevel(self.root)
        self.top.overrideredirect(True)
        self.top.geometry(MAIN_WINDOW_SIZE)
        self.top.title(APPLICATION_NAME)
        self.is_maximized = False
        self.root.attributes("-alpha", 0.0)
        app_icon_path = os.path.join(IMAGES_DIR, 'code-snippet.png')
        self.top.iconphoto(True, PhotoImage(file=app_icon_path))
        self.root.bind("<Unmap>", self.onrooticonify)
        self.root.bind("<Map>", self.onrootdeiconify)
        self.center_window(self.top)

        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

    def center_window(self, window):
        """
        Summary
        """
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

    def initialize_ui(self):
        """
        Central method for initializing the UI. This method is responsible for applying the selected theme,
        setting up the custom title bar, and creating the primary widgets of the application.
        """
        self.apply_theme()
        self.setup_custom_title_bar()
        self.create_widgets()

    def apply_theme(self):
        """
        Applies the currently selected theme to the application's UI elements.

        This method retrieves the current theme settings from the ThemeManager and applies these settings
        to various UI components of the application, such as background colors, fonts, and other stylistic elements.
        It ensures that the application's appearance is consistent with the user's theme preferences.
        """
        # Access the current theme from theme_manager
        current_theme = theme_manager.get_current_theme()

        # Apply theme to tk widgets
        self.top.configure(background=current_theme['colors']['background'])

        # Initialize a ttk Style
        self.style = ttk.Style(self.top)

        try:
            # Apply theme to ttk widgets through styles
            for widget_style, settings in current_theme['ttkStyles'].items():
                style_name = widget_style + ".TButton" if widget_style != "TButton" else "TButton"
                try:
                    map_settings = settings.get('map', {})

                    # Convert the 'map' settings back to the expected format (list of tuples)
                    converted_map_settings = {
                        key: [(state, value) for state_dict in values for state, value in state_dict.items()] for
                        key, values in map_settings.items()}

                    self.style.configure(style_name, **settings.get('configure', {}))
                    self.style.map(style_name, **converted_map_settings)
                except Exception as e:
                    logger.error(f"Error applying theme to {style_name}: {e}")
        except Exception as e:
            logger.error(f"Error applying theme: {e}")
            # Optionally, apply a default style or handle the error in a way that
            # ensures the application remains usable.

    def setup_custom_title_bar(self):
        """Configures the custom title bar with minimize, maximize, and close buttons."""

        self.minimize_img = self.load_image_with_pil(os.path.join(IMAGES_DIR, 'minimize-window-48.png'), width=16,
                                                     height=16)
        self.maximize_img = self.load_image_with_pil(os.path.join(IMAGES_DIR, 'maximize-window-48.png'), width=16,
                                                     height=16)
        self.close_img = self.load_image_with_pil(os.path.join(IMAGES_DIR, 'close-window-48.png'), width=16, height=16)

        self.title_bar = ttk.Frame(self.top, relief="raised")
        self.title_bar.pack(fill=tk.X)
        self.title_label = ttk.Label(self.title_bar, text=APPLICATION_NAME)
        self.title_label.pack(side=tk.LEFT, padx=10)

        # Close Button
        self.close_button = ttk.Button(self.title_bar, image=self.close_img, command=self.close_window,
                                       style="ImageButton.TButton")
        self.close_button.pack(side=tk.RIGHT)

        # Maximize/Restore Button
        self.max_button = ttk.Button(self.title_bar, image=self.maximize_img, command=self.maximize_restore_window,
                                     style="ImageButton.TButton")
        self.max_button.pack(side=tk.RIGHT)

        # Minimize Button
        self.min_button = ttk.Button(self.title_bar, image=self.minimize_img, command=self.minimize_window,
                                     style="ImageButton.TButton")
        self.min_button.pack(side=tk.RIGHT)

        self.title_bar.bind("<B1-Motion>", self.drag_window)
        self.title_bar.bind("<Button-1>", self.get_pos)
        self.title_bar.bind("<Double-1>", self.toggle_maximize_restore)  # Maximize/Restore on double-click

    def load_image_with_pil(self, path, width, height):
        # Open the image file
        img = Image.open(path)
        # Resize it to the width and height specified using LANCZOS resampling
        img = img.resize((width, height), Image.Resampling.LANCZOS)
        # Convert to a format Tkinter can handle
        return ImageTk.PhotoImage(img)

    def minimize_window(self):
        """
        Minimizes the application window to the system tray or taskbar.

        This method is typically bound to a minimize button in a custom title bar. It triggers the standard
        window minimization behavior, effectively hiding the window from the screen without closing the application.
        """
        self.root.update_idletasks()
        self.root.iconify()

    def on_hover(self, event):
        event.widget.config(bg="#ff0000")  # Change color on hover

    def on_leave(self, event):
        event.widget.config(bg="#FFFFFF")  # Original color

    def toggle_maximize_restore(self, event):
        """
        Toggles the window between its maximized and restored states when the title bar is double-clicked.

        Args:
            event: A tkinter event object containing information about the double click action.
        """
        self.maximize_restore_window()

    def maximize_restore_window(self):
        """
        Toggles the application window between its maximized state and its original size.

        This method is responsible for expanding the application window to fill the entire screen when not
        maximized and restoring it to its previous dimensions when maximized. It's commonly linked to a
        maximize/restore button in a custom title bar.
        """
        if self.is_maximized:
            self.top.geometry(self.prev_geom)
            self.is_maximized = False
        else:
            self.prev_geom = self.top.geometry()
            self.top.geometry("{0}x{1}+0+0".format(
                self.top.winfo_screenwidth(), self.top.winfo_screenheight()))
            self.is_maximized = True

    def drag_window(self, event):
        """
        Allows the user to drag the window around the screen by clicking and holding the custom title bar.

        Args:
            event: A tkinter event object that contains the mouse cursor's current x and y coordinates.
        """
        x, y = event.x_root, event.y_root
        self.top.geometry(f"+{x - self.offset_x}+{y - self.offset_y}")

    def close_window(self):
        """
        Closes the application window and terminates the application.

        This method should be connected to a close button in a custom title bar. It ensures that the application
        shuts down gracefully when the user decides to exit.
        """
        self.callbacks["close_db_connection"]()
        self.root.destroy()

    def onrooticonify(self, event):
        """
        Handles the event when the main application window is minimized. This method is triggered
        automatically by tkinter when the application window is iconified (minimized).

        Args:
            event: A tkinter event object representing the iconify action.
        """
        self.top.withdraw()

    def onrootdeiconify(self, event):
        """
        Handles the event when the main application window is restored from being minimized. This method
        is triggered automatically by tkinter when the application window is deiconified (restored).

        Args:
            event: A tkinter event object representing the deiconify action.
        """
        self.top.deiconify()

    # Function to print style information
    def print_style_info(self, widget_style):
        """
        Prints detailed style information for a given ttk widget style to the console. This method is useful
        for debugging and understanding the current style configuration of ttk widgets.

        Args:
            widget_style: The name of the ttk widget style to print information for (e.g., "TButton").
        """
        print("Style Configuration for:", widget_style)
        # Print the settings for the widget style
        print(self.style.configure(widget_style))
        # Print layout information (might not directly correspond to 'configure' settings)
        print("Layout:", self.style.layout(widget_style))
        # Print specific style options (e.g., background color)
        print("Background Color:", self.style.lookup(widget_style, 'background'))
        print("Foreground Color:", self.style.lookup(widget_style, 'foreground'))

    def create_widgets(self):
        """Create GUI widgets, including the ribbon and snippet display area."""
        self.setup_ribbon()
        self.setup_snippet_display()

    def setup_ribbon(self):
        """Set up the ribbon."""
        self.notebook = ttk.Notebook(self.top)
        self.notebook.pack(fill='x')
        self.setup_home_tab(ttk.Frame(self.notebook), 'Home')
        self.setup_categories_tab(ttk.Frame(self.notebook), 'Languages & Categories')
        self.setup_tools_tab(ttk.Frame(self.notebook), 'Tools')
        self.setup_settings_tab(ttk.Frame(self.notebook), 'Settings')
        self.setup_feedback_and_help_tab(ttk.Frame(self.notebook), 'Feedback & Help')

    def setup_home_tab(self, tab, title):
        """Set up the home tab."""
        self.notebook.add(tab, text=title)
        self.new_snippet_btn = ttk.Button(tab, text='New Snippet', command=self.callbacks['new_snippet'])
        self.edit_snippet_btn = ttk.Button(tab, text='Edit Snippet', command=self.callbacks['edit_snippet'])
        self.delete_snippet_btn = ttk.Button(tab, text='Delete Snippet', command=self.callbacks['delete_snippet'])

        # Add buttons to the tab
        self.new_snippet_btn.pack(side='left', padx=5)
        self.edit_snippet_btn.pack(side='left', padx=5)
        self.delete_snippet_btn.pack(side='left', padx=5)

    def setup_categories_tab(self, tab, title):
        """Set up the categories tab."""
        self.notebook.add(tab, text=title)
        manage_languages_btn = ttk.Button(tab, text='Manage languages')
        manage_categories_btn = ttk.Button(tab, text='Manage Categories')

        # Add buttons and dropdown menu to the tab
        manage_languages_btn.pack(side='left', padx=5)
        manage_categories_btn.pack(side='left', padx=5)

    def setup_tools_tab(self, tab, title):
        """Set up the tools tab."""
        self.notebook.add(tab, text=title)
        import_snippets_btn = ttk.Button(tab, text='Import Snippets', command=self.callbacks['import_snippet'])
        export_snippets_btn = ttk.Button(tab, text='Export Snippets', command=self.callbacks['export_snippet'])

        # Add buttons to the tab
        import_snippets_btn.pack(side='left', padx=5)
        export_snippets_btn.pack(side='left', padx=5)

    def setup_settings_tab(self, tab, title):
        """Set up the tools tab."""
        self.notebook.add(tab, text=title)
        manage_theme_btn = ttk.Button(tab, text='Manage Themes', command=self.callbacks['generate_code'])
        manage_configuration_btn = ttk.Button(tab, text='Manage Configuration',
                                              command=self.callbacks['open_preferences'])

        # Add buttons to the tab
        manage_theme_btn.pack(side='left', padx=5)
        manage_configuration_btn.pack(side='left', padx=5)

    def setup_feedback_and_help_tab(self, tab, title):
        """Set up the Feedback & Help tab."""
        self.notebook.add(tab, text=title)
        self.help_btn = ttk.Button(tab, text='User Guide')  # , command=self.callbacks['open_user_guide'])
        self.faq_btn = ttk.Button(tab, text='FAQs')  # , command=self.callbacks['open_faqs'])
        self.report_issue_btn = ttk.Button(tab, text='Report Issue')  # , command=self.callbacks['report_issue'])
        self.suggest_feature_btn = ttk.Button(tab, text='Suggest Feature')  # , command=self.callbacks['suggest_feature'])
        self.about_btn = ttk.Button(tab, text='About', command=self.open_about())

        # Add buttons to the tab
        self.help_btn.pack(side='left', padx=5)
        self.faq_btn.pack(side='left', padx=5)
        self.report_issue_btn.pack(side='left', padx=5)
        self.suggest_feature_btn.pack(side='left', padx=5)
        self.about_btn.pack(side='left', padx=5)

    def setup_snippet_display(self):
        """Set up the snippet display."""
        # Parent frame for displaying code snippets
        snippet_display_frame = ttk.Frame(self.top)
        snippet_display_frame.pack(fill='both', expand=True)

        # Frame for treeview
        treeview_frame = ttk.Frame(snippet_display_frame)
        treeview_frame.pack(side='left', fill='both', expand=True)

        # Label for the treeview
        treeview_label = ttk.Label(treeview_frame, text='Snippets')
        treeview_label.pack(side='top', pady=5)

        # Treeview for displaying snippets
        self.treeview = ttk.Treeview(treeview_frame)
        self.treeview.pack(side='top', fill='both', expand=True)
        self.treeview.bind('<<TreeviewSelect>>', self.on_selection_change)

        # Frame for code text
        code_text_frame = ttk.Frame(snippet_display_frame)
        code_text_frame.pack(side='left', fill='both', expand=True)

        # Label for the code text area
        code_text_label = ttk.Label(code_text_frame, text='Snippet Details')
        code_text_label.pack(side='top', pady=5)

        # Textblock for displaying code
        self.code_text = tk.Text(code_text_frame)
        self.code_text.pack(side='top', fill='both', expand=True)

        self.treeview.bind('<Button-1>', self.on_tree_click)

    def on_tree_click(self, event):
        """
        summary
        """
        # Identify the item under the cursor
        item = self.treeview.identify_row(event.y)
        if not item:
            # Click was not on an item
            self.last_clicked_item = None
            return

        current_selection = self.treeview.selection()
        if item == self.last_clicked_item:
            # Click is on the previously clicked item, toggle selection
            if item in current_selection:
                self.treeview.selection_remove(item)
            else:
                self.treeview.selection_add(item)
        else:
            # Different item clicked, update selection normally
            self.treeview.selection_set(item)

        self.last_clicked_item = item  # Update the last clicked item

    def clear_code_text(self):
        """Clears the contents of the code_text widget."""
        self.code_text.delete('1.0', tk.END)

    def get_pos(self, event):
        """ summary """
        self.offset_x = event.x
        self.offset_y = event.y

    def update_general_categories(self, general_categories_returned):
        """ summary
        """
        self.general_categories = general_categories_returned

    def update_language_specific_categories(self, language_specific_categories_returned):
        """Updates the stored language-specific categories with the provided dictionary."""
        self.language_specific_categories = language_specific_categories_returned

    def refresh_treeview(self, structured_data):
        """ refresh the treeview with the provided structured """
        self.treeview.delete(*self.treeview.get_children())

        for lang_id, lang_info in structured_data.items():
            # Add language node
            lang_node = self.treeview.insert('', 'end', text=lang_info['name'])

            # Add category nodes under language
            for cat_key, cat_info in lang_info['categories'].items():
                cat_node = self.treeview.insert(lang_node, 'end', text=cat_info['name'])

                # Add snippet nodes under category
                for snippet in cat_info['snippets']:
                    self.treeview.insert(cat_node, 'end', iid=f"snippet-{snippet['id']}", text=snippet['title'],
                                         values=(snippet['id'],))

    def update_ui_based_on_preferences(self, new_preferences):
        """Updates the treeview with the provided list of snippets."""
        # Update UI elements based on new preferences

    def on_selection_change(self, event=None):
        """
        Called when the selection changes in the treeview. It updates the application
        based on the current selection. If there is no selection, it clears the
        previously shown details.
        """
        current_selection = self.treeview.selection()

        if current_selection:
            # There's a selection, handle the selection
            current_item = current_selection[0]  # Assuming single selection mode

            if current_item != self.last_selected_item:
                # The selection has changed, proceed with the action
                self.last_selected_item = current_item
                self.callbacks["on_tree_select"](current_item)
                # Additional actions based on the selection can be placed here
        else:
            # No selection, clear the displayed details
            self.clear_code_text()
            self.last_selected_item = None  # Clear the last selected item tracking

    def display_snippet_code(self, code):
        """
        Summary
        """
        self.code_text.delete('1.0', tk.END)  # Clear the current content
        self.code_text.insert('1.0', code)  # Insert the new code

    def run(self):
        """
        Initiates the application's main loop, making the application window visible and responsive to user actions.
        """
        window = tkinter.Frame(master=self.top)
        window.mainloop()
