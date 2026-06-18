from .map_parser import Loop_Through
from sys import argv
from .motor import Motor

val = Loop_Through()
for i, v in enumerate(val):
    print(v)

visual = Motor()
visual.VisualLoop()