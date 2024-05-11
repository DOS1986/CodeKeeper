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
import json
import os
import tkinter as tk


class Highlighter:
    """
    A syntax highlighting service for Tkinter Text widgets.

    This class provides syntax highlighting functionality by applying text tags
    to patterns within a Tkinter Text widget. It is designed to be flexible and
    easily extendable to support various programming languages by loading syntax
    highlighting rules from JSON files.

    The highlighting rules are expected to define patterns for different syntax
    elements such as keywords, comments, strings, etc. This class uses regular
    expressions to match these patterns within the text content of a Text widget
    and applies the corresponding Tkinter text tags to highlight them.

    Attributes:
        rules (dict): A dictionary containing the syntax highlighting rules loaded
                      from a JSON file. This includes patterns for keywords, comments,
                      and other syntax elements specific to the programming language.

    Methods:
        __init__(language): Initializes the Highlighter with syntax rules for the specified
                            programming language.
        load_rules(language): Loads the syntax rules from a JSON file corresponding to
                              the specified programming language.
        apply(text_widget): Applies syntax highlighting to the given Text widget based on
                            the loaded rules.
        highlight_pattern(text_widget, pattern, tag, nocase, regexp): Searches for the given
                                                                       pattern in the Text widget
                                                                       and applies the specified tag
                                                                       to highlight matches. Supports
                                                                       case-sensitive and insensitive
                                                                       searches, and can handle regular
                                                                       expression patterns.
    Example:
        >>> from tkinter import Tk, Text
        >>> root = Tk()
        >>> text_widget = Text(root)
        >>> text_widget.pack()
        >>> highlighter = Highlighter("python")
        >>> highlighter.apply(text_widget)
        >>> root.mainloop()

    Note:
        - The JSON file containing syntax rules should be placed in a 'syntax' directory
          relative to this script.
        - Each syntax rule file should be named after the programming language it represents
          (e.g., 'python.json' for Python syntax rules).
    """
    def __init__(self, language):
        """
        Initialize the Highlighter with language-specific syntax rules.

        Args:
            language (str): The programming language to load syntax rules for.
        """
        self.rules = self.load_rules(language)

    def load_rules(self, language):
        """
        Load syntax highlighting rules from a JSON file for the specified language.

        Args:
            language (str): The programming language whose rules are to be loaded.

        Returns:
            dict: The syntax rules for the specified language.
        """
        # Define the directory path where syntax rule JSON files are stored
        syntax_dir = os.path.join(os.path.dirname(__file__), 'syntax')
        file_path = os.path.join(syntax_dir, f"{language}.json")
        with open(file_path, 'r') as file:
            return json.load(file)

    def apply(self, text_widget):
        """
        Apply syntax highlighting to the given text widget based on loaded rules.

        Args:
            text_widget (tk.Text): The text widget to which syntax highlighting is applied.
        """
        # First, remove any existing tags to reset the highlighting
        for tag in text_widget.tag_names():
            text_widget.tag_remove(tag, "1.0", "end")

        # Apply highlighting for each type of syntax rule (e.g., keywords, comments)
        for rule_type, rules in self.rules.items():
            if rule_type == "keywords":
                for keyword in rules:
                    self.highlight_pattern(text_widget, r'\m{}\M'.format(keyword), "keyword", nocase=0)
            elif rule_type == "comments":
                self.highlight_pattern(text_widget, r'{}.*$'.format(rules["single_line"]), "comment", nocase=0)

    def highlight_pattern(self, text_widget, pattern, tag, nocase=1, regexp=False):
        """
        Highlight all instances of a specified pattern within a text widget.

        This method uses the text widget's search functionality to find and highlight
        all occurrences of a given pattern. It allows for both case-sensitive and
        case-insensitive searches, and can handle regular expression patterns.

        Args: text_widget (tk.Text): The text widget where the pattern is to be highlighted. pattern (str): The regexp
        pattern to search for within the text widget. tag (str): The name of the tag used to highlight the matched
        patterns. nocase (int): If set to 1, the search is case-insensitive; if 0, the search is case-sensitive.
        regexp (bool): If True, the pattern is treated as a regular expression. If False, the pattern is treated as
        plain text.
        """
        # Set the start index for the search to the beginning of the text widget
        start = text_widget.index("1.0")
        # Set the end index for the search to the end of the text widget
        end = text_widget.index("end")
        # Initialize the search start and end markers in the text widget
        text_widget.mark_set("matchStart", start)
        text_widget.mark_set("matchEnd", start)
        text_widget.mark_set("searchLimit", end)

        # Variable to hold the length of the matched string
        count = tk.IntVar()
        while True:
            # Perform the search from the last match end to the search limit
            index = text_widget.search(pattern, "matchEnd", "searchLimit", count=count, nocase=nocase, regexp=regexp)
            if index == "":
                break  # Exit the loop if no more matches are found
            if count.get() == 0:
                break  # Exit the loop if the match length is 0 to prevent infinite loops
            # Update the match start and end markers based on the current match
            text_widget.mark_set("matchStart", index)
            text_widget.mark_set("matchEnd", "%s+%sc" % (index, count.get()))
            # Apply the specified tag to the current match
            text_widget.tag_add(tag, "matchStart", "matchEnd")
