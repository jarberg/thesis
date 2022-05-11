import os
import sys
import src.utils.constants as constants


constants.ROOT_DIR = "{}/src".format(os.path.dirname(sys.modules['__main__'].__file__))