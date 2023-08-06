import os
import sys


def get_clipfree_path():
    """Returns the path hordelib is installed in."""
    current_file_path = os.path.abspath(__file__)
    return os.path.dirname(current_file_path)

