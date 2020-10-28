from SeleniumLibrary.base.robotlibcore import HybridCore
from .Actions import Main
from .Actions import main
import sys


class Share(HybridCore):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        library = ([main])
        HybridCore.__init__(self, library)
        self.add_library_components(
            [
                Main(self)
            ]
        )
        ####################################################################################
        # Make sure pydevd installed: pip install pydevd
        # AND Uncomment following codes to enable debug mode
        # sys.path.append("pycharm-debug-py3k.egg")
        # import pydevd
        # pydevd.settrace('localhost', port=8001, stdoutToServer=True, stderrToServer=True)
        ####################################################################################
