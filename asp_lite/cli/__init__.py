from sys import stdin, stdout

from ..transpile import transpile
from ..format    import format

def main_transpile():
    transpile(stdin, stdout)

def main_format():
    format(stdin, stdout)
