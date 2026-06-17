from .map_parser import Loop_Through
from sys import argv
from .motor import screen

val = Loop_Through()
for i, v in enumerate(val):
    print(v)

visual = screen(150)
