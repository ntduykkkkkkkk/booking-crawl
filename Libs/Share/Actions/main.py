from SeleniumLibrary.base import keyword, LibraryComponent
import os
import json

__version__ = '1.0.0'


class Main(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def get_root_path(self):
        current_path = os.path.dirname(os.path.dirname(__file__))
        return os.path.dirname(os.path.dirname(os.path.join("..", current_path)))

    @staticmethod
    def format_os_path(path):
        # /: Linux
        # \: Windows
        return path.replace('\\', '/') if os.sep == '/' else path.replace('/', '\\')

    @keyword
    def get_setup_data(self):
        with open(Main.get_root_path(self) + Main.format_os_path("\\Resources\\setup.json")) as f:
            return json.loads(f.read())
