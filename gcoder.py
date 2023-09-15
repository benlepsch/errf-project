'''
Ben Lepsch

program will:
- take a gcode file
- remove home all command, replace with home x and z
- at end of gcode move conveyor belt one full rotation + a little bit extra to even out wear

so
open a dialog box

    |----------------------------------------|
    | GCODE fixer                          X |
    |----------------------------------------|
    | Select File: <Browse>                  |
    |                                        |
    | Output path + filename:                |
    | (input box here, set default path?)    |
    |                                        |
    | <Fix GCODE>       <Open Config File>   |
    |----------------------------------------|

something to this effect
i am thinking config file so you can change conveyor belt full rotation value
could also just do this as a preset at first

'''

from tkinter import filedialog