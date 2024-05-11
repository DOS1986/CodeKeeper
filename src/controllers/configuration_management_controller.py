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


class ConfigurationController:
    """
            summary
    """

    def __init__(self, model, application_callbacks):
        """
                summary
        """
        self.model = model
        self.view = None
        self.application_callbacks = application_callbacks
        self.callbacks = {
            'load_configuration': self.load_configuration
        }

    def set_view(self, view):
        """ set """
        self.view = view

    def load_configuration(self, name):
        """ summary """
        config_data = self.model.read_config(name)
        return config_data

    def get_callbacks(self):
        """ set """
        return self.callbacks

    def run_application(self):
        """ summary """
        # Display initial state of the application
        if self.view:
            self.view.run()

    def apply_configurations(self, new_configurations):
        """
        summary
        """
        self.model.update_configurations(new_configurations)
