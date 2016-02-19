import sys
import os

_tests_folder = os.path.dirname(__file__)
_lib_folder = os.path.abspath(os.path.join('..', _tests_folder))

sys.path.append(_lib_folder)
