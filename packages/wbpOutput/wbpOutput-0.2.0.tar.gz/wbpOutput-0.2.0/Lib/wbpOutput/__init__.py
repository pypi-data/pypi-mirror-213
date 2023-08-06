"""
Implementation of the output plugin.
"""

from .outputwin import outputPanel
from .preferences import OutputWinPreferences

__version__ = "0.2.0"

panels = [outputPanel]
preferencepages = [OutputWinPreferences]
