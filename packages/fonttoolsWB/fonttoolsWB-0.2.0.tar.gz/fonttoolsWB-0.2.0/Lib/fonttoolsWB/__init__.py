"""
FontTools WorkBench Edit OpenType fonts as XML
"""

import wbBase

__version__ = "0.2.0"

class App(wbBase.application.App):
    """
    FontTools WorkBench application.

    Each WorkBench application needs its own application class in order to  
    allow the python importlib to find application resources and plugins.
    """

